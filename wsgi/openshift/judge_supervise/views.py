from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse

from collections import defaultdict

from openshift.contest.models import Contest, Team
from openshift.execution.models import Problem
from openshift.helpFunctions.views import getTodayDate
from openshift.teamsubmission.models import Submission, ExecutionLogEntry

from .html_view_classes import CountFeedbackRow, ProblemAttempsCount,\
                               SubFeedbackView, TeamSummaryRow

def date_in_range(dateobject, start, end):
    return (start <= dateobject and dateobject  <= end)

def get_team_assignments(team_list):
    onsite_list, offsite_list = [], []
    for team in team_list:
        submissions = Submission.objects.filter(team=team) \
                      .order_by('-date_uploaded').order_by('problem')

        prob_to_subs_dict = defaultdict( list )
        solved_count = 0
        for sub in submissions:
            if sub.solved_problem == True:
                solved_count += 1
            prob_to_subs_dict[sub.problem].append(sub)

        for prob in prob_to_subs_dict:
            sub_list = prob_to_subs_dict[prob]

            if team.onsite == True:
                stfv = TeamSummaryRow(team=team,
                                         fail_count=len(sub_list),
                                         prev_solved=solved_count )
                onsite_list.append(stfv)
            else:
                stfv = TeamSummaryRow(team=team,
                                         fail_count=len(sub_list),
                                         prev_solved=solved_count,
                                         site_location = team.offsite)
                offsite_list.append(stfv)

    return onsite_list, offsite_list

def get_current_contest():
    today = getTodayDate()
    contests = Contest.objects.all()

    return next((date_in_range(today, con.start_date, con.end_date) \
                 for con in contests))


def get_most_plausible_contest(contest_pk):
    given_contest = None
    if contest_pk:
        try:
            given_contest = Contest.objects.get(id=contest_pk)
        except TypeError:
            pass

    return given_contest  or get_current_contest() \
                          or Contest.objets.earliest('teamreg_end_date')

def get_attempt_count(contest):
    problems = Problem.objects.filter(contest=contest).order_by('title')
    submissions = Submission.objects.get_queryset()
    groups = defaultdict( list )
    ret_list = [ ]

    for sub in submissions:
        groups[sub.problem].append(sub)

    for prob in problems:
        failed_for_problem, succeded_for_problem = 0, 0
        for sub in groups[prob]:

            if sub.solved_problem:
                succeded_for_problem += 1
            else:
                failed_for_problem += 1

        ret_list.append( ProblemAttempsCount(problem=prob,
                                            failed=failed_for_problem,
                                            successfull=succeded_for_problem
                                            ))
    return ret_list

def judge_submission_team(request, team_pk, problem_pk):
    submissions = Submission.objects.filter(team=team_pk) \
                    .order_by('-date_uploaded').filter(problem=problem_pk)
    sub_feed_items = []

    for sub in submissions:
        sub_feed_items.append( SubFeedbackView(sub) )

    context = {
            'sub_feed_items' : sub_feed_items,
            'team': Team.objects.get(pk=team_pk),
            }

    return render(request,
                  'judge_team_summary.html',
                  context)

def judge_team_summary(request, team_pk):
    """ The page to render an overview of the team
    """
    feedback_prob_dict = dict()
    feedback_dict = dict()
    submissions = Submission.objects.filter(team=team_pk)\
                  .exclude(executionlogentry__isnull=True)\
                  .order_by('-date_uploaded')
    # TODO: get code

    feedbacks = ExecutionLogEntry.objects.all()
    prob_row, sub_feed_items = [], []
    prob_index = {}
    problems = Problem.objects.get_queryset() # all problems

    for index, problem in enumerate(problems):
        prob_index[problem] = index

    for feedback in feedbacks:
        feedback_dict[feedback.submission] = feedback

    for sub in submissions:
        feedback = None
        if sub in feedback_dict:
            feedback = feedback_dict[sub]

        # Put the feedback in to dict
        # , or, if empty, put an empty array
        feedback_prob_dict.setdefault(feedback, [0] * len(problems))
        # Assuming the the prob_index[sub.problem] points to the
        # the same order as in `problems`. This should be valid since
        # the enumerate above
        feedback_prob_dict[feedback][prob_index[sub.problem]] += 1

        sub_feed_items.append( SubFeedbackView(sub, feedback))

    total_count = dict([(feedback,sum(problems)) \
                    for feedback,problems in feedback_prob_dict.iteritems()])

    for key, val in feedback_prob_dict.iteritems():
        prob_row.append(CountFeedbackRow(feedback = key,
                                         total=total_count[key],
                                         prob_count_list = val))

    context = {
            'sub_feed_items' : sub_feed_items,
            'problems'       : problems,
            'prob_row'       : prob_row,
            'team'           : Team.objects.get(pk=team_pk),
            }

    return render(request,
                  'judge_team_summary.html',
                  context)


def judge_home(request, contest_pk=None):
    contest = get_most_plausible_contest(contest_pk)

    if not contest: # if there are no contests
        return HttpResponse('<h1> There are no contests in the database </h1>')

    try:
        team_list = Team.objects.filter(contest=contest)
    except ObjectDoesNotExist:
        team_list = []


    prob_attempt_counts = get_attempt_count(contest)

    team_tr_row_info_onsite, team_tr_row_info_offsite = \
                                                get_team_assignments(team_list)

    context = {
            'contests'            : Contest.objects.all(),
            'contest'             : contest,
            'team_list'           : team_list,
            'team_tr_row_info_onsite'   : team_tr_row_info_onsite,
            'team_tr_row_info_offsite'  : team_tr_row_info_offsite,
            'prob_attempt_counts' : prob_attempt_counts,
            }

    return render(request,
                  'judge_home.html',
                  context,
                  )

# EOF
