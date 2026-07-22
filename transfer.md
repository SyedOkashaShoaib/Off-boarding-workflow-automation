(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git log --follow --date=short --format="%h %ad %s" -- app/templates/workflow/task_detail.html
6008177 2026-07-22 add accountable checklist response controls
64f038d 2026-07-15 cleaned task_deatil and admin_approval function
d01e347 2026-07-15 fixed admin approval function bug
feabb01 2026-07-15 cleaned application shell and feedback behavior
4adfc57 2026-07-13 Update task_detail.html
cff1056 2026-07-13 workflow route
611cb47 2026-07-13 Create task_detail.html
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git ls-files | Select-String -Pattern 'task-detail | task_checklist | checklist'
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git log --all --date=short --format="COMMIT %h %ad %s" --name-status --app/templates/workflow/task_detail.html
fatal: unrecognized argument: --app/templates/workflow/task_detail.html
(.venv) PS C:\Users\intern\Desktop\intern_summer_26\offboarding_workflow> git log --all --date=short --format="COMMIT %h %ad %s" --name-status -- app/templates/workflow/task_detail.html
COMMIT 6008177 2026-07-22 add accountable checklist response controls

M       app/templates/workflow/task_detail.html
COMMIT d18e8d2 2026-07-20 Revert "Feature/admin token access"

D       app/templates/workflow/task_detail.html
COMMIT 5f0b397 2026-07-16 restore secure task access entry ponit

M       app/templates/workflow/task_detail.html
COMMIT 363d564 2026-07-15 refine dep task workflow

M       app/templates/workflow/task_detail.html
COMMIT b45015b 2026-07-15 Update task_detail.html

M       app/templates/workflow/task_detail.html
COMMIT 64f038d 2026-07-15 cleaned task_deatil and admin_approval function

M       app/templates/workflow/task_detail.html
COMMIT d01e347 2026-07-15 fixed admin approval function bug

M       app/templates/workflow/task_detail.html
COMMIT 5e797f2 2026-07-15 Update task_detail.html

M       app/templates/workflow/task_detail.html
COMMIT feabb01 2026-07-15 cleaned application shell and feedback behavior

M       app/templates/workflow/task_detail.html
COMMIT 4adfc57 2026-07-13 Update task_detail.html

M       app/templates/workflow/task_detail.html
COMMIT cff1056 2026-07-13 workflow route

A       app/templates/workflow/task_detail.html
