import base64, os, sys

employees = env['hr.custom.employee'].search([])
updated = 0
for emp in employees:
    if emp.image_1920:
        continue
    if not emp.position:
        continue
    path = '/mnt/extra-addons/isil_hr_advanced/static/img/{}.png'.format(emp.position)
    if os.path.isfile(path):
        with open(path, 'rb') as f:
            emp.image_1920 = base64.b64encode(f.read())
        updated += 1

env.cr.commit()
print('Backfilled {} employees'.format(updated))
