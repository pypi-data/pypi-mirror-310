#!/usr/bin/env python
import logging
import os
from pathlib import Path

from edc_test_utils import DefaultTestSettings, func_main

app_name = "edc_csf"
base_dir = Path(__file__).absolute().parent

project_settings = DefaultTestSettings(
    calling_file=__file__,
    template_dirs=[os.path.join(base_dir, app_name, "tests", "templates")],
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    EDC_SITES_REGISTER_DEFAULT=True,
    SUBJECT_VISIT_MODEL="edc_visit_tracking.subjectvisit",
    SUBJECT_VISIT_MISSED_MODEL="edc_appointment.subjectvisitmissed",
    SUBJECT_REQUISITION_MODEL="edc_csf_app.subjectrequisition",
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "simple_history",
        "multisite",
        "django_crypto_fields.apps.AppConfig",
        "edc_action_item.apps.AppConfig",
        "edc_visit_tracking.apps.AppConfig",
        "edc_notification.apps.AppConfig",
        "edc_lab.apps.AppConfig",
        "edc_appointment.apps.AppConfig",
        "edc_timepoint.apps.AppConfig",
        "edc_offstudy.apps.AppConfig",
        "edc_visit_schedule.apps.AppConfig",
        "visit_schedule_app.apps.AppConfig",
        "edc_crf.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_metadata.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_csf.apps.AppConfig",
        "edc_csf_app.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
).settings


def main():
    func_main(project_settings, f"{app_name}.tests")


if __name__ == "__main__":
    logging.basicConfig()
    main()
