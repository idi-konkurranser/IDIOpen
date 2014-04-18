from django.contrib import admin
from .models import MessageAnswer, Message
# Register your models here.

class MessageAnswerAdmin(admin.ModelAdmin):
    list_display = ('subject', 'answered_by', 'answered_at', 'message')
    fields = ('subject', 'body', 'contest')
    
    def save_model(self, request, obj, form, change):
        if form.changed_data:
            if 'answered' in form.changed_data: 
                obj.save()
            # Set answered to True, if not specified by the admin
            else:
                obj.answered = True
        obj.save()
 
class AnswerInline(admin.TabularInline):
    model = MessageAnswer
    # Don't show any extra MessageAnswer's on default
    extra = 0
    fields = ('subject', 'body', 'answered_by',)
    readonly_fields = ('answered_by',)
    
        
class MessageAdmin(admin.ModelAdmin):
    inlines = (AnswerInline,)
    list_display = ('subject', 'sender', 'sent_at', 'answered',)
    list_filter = ('sent_at',)
    date_hierarchy = 'sent_at'
    ordering = ('-sent_at', '-answered')
    readonly_fields = ('subject', 'body', 'sender', 'contest')
    
    # Set answered_by and contest fields for the MessageAnswers before saving them
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.answered_by = request.user
            instance.contest = instance.message.contest
            instance.save()
        formset.save_m2m()
    
    # Set Message.answered = True, when saving.     
    def save_model(self, request, obj, form, change):
        # Check if the form has changed
        if form.changed_data:
            if 'answered' in form.changed_data: 
                obj.save()
            # Set answered to True, if not specified by the admin
            else:
                obj.answered = True
        obj.save()
        
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageAnswer, MessageAnswerAdmin)