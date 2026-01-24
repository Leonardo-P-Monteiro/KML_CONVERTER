
.PHONY: git_commit, set_dev_conf, runserver

git_commit:
	git add . && git commit -m 'att' && git push origin main 

set_dev_conf:
	export DJANGO_SETTINGS_MODULE=config.settings.development

runserver:
	python manage.py runserver_plus --cert-file cert.crt