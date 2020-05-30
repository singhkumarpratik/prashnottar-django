from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django_comments_xtd.admin import XtdCommentsAdmin
from comments.models import MyComment


class MyCommentAdmin(XtdCommentsAdmin):
    list_display = (
        "thread_level",
        "cid",
        "name",
        "content_type",
        "object_pk",
        "submit_date",
        "followup",
        "is_public",
        "is_removed",
        "vote_score",
    )
    list_display_links = ("cid",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "content_type",
                    "object_pk",
                    "site",
                    "vote_score",
                    "num_vote_up",
                    "num_vote_down",
                )
            },
        ),
        (
            _("Content"),
            {
                "fields": (
                    "user",
                    "user_name",
                    "user_email",
                    "user_url",
                    "comment",
                    "followup",
                )
            },
        ),
        (
            _("Metadata"),
            {"fields": ("submit_date", "ip_address", "is_public", "is_removed")},
        ),
    )


admin.site.register(MyComment, MyCommentAdmin)
