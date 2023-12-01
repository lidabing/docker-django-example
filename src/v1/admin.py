# Register your models here.
from django.contrib import admin

from .models import V1Model
from .tasks import slow_task


class V1ModelAdmin(admin.ModelAdmin):
    actions = ["execute_slow_task"]

    def execute_slow_task(self, request, queryset):
        # 在这里执行slow_task
        print("execute_slow_task")
        slow_task()
        self.message_user(request, "Slow task has been started.")

    slow_task.short_description = "Execute slow task"


admin.site.register(V1Model, V1ModelAdmin)
