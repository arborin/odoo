#import libraries
import os

os.system('cls' if os.name == 'nt' else 'clear')

#create folder structure
cwd = os.getcwd()
print(">>>>> CREATING ODOO v8 MODULE <<<<<")
print('-'*50)
print("""
    Module base structure
    
    module_dir/
        | __init__.py
        | __openerp__.py
        | module_name.py
        | module_name_view.xml
        | security/
        |    | module_name_security.xml
        |    | ir.model.access.csv
        | report/
        |    | __init__.py
        |    | module_name_report_view.xml
        |    | module_name_report.py
        |    | module_name_report.mako
      """)

print('-'*50)
module_name = input("1. Enter module name: ").lower()
module_name = module_name
print('>> Set module name: {}'.format(module_name))
print("2. Default path is: [{}]".format(cwd))
path = input("   Enter another path or press enter: ")
            	 
if not path:
	path = cwd

dir_name = module_name
if " " in module_name:
    dir_name = module_name.replace(" ","_")
    
path = os.path.join(path, dir_name)
print(">> Set module Path: {}".format(path))
#create module directory
if not os.path.exists(path):
	os.makedirs(path)
# security dir
security_dir = os.path.join(path,"security")

if not os.path.exists(security_dir):
	os.makedirs(security_dir)

file = open(os.path.join(security_dir, dir_name+"_security.xml"), 'w+')
file.close()
file = open(os.path.join(security_dir, "ir.model.access.csv"), 'w+')
file.close()


module_desc = input("3. Module description [optional]: ").capitalize()
print(">> Set module description {}".format(module_desc))
module_author = input("4. Module author [optional]: ").capitalize()
print(">> Set module author {}".format(module_desc))
print('-'*50)
print("""
    View Structure
    
    ----------------------------------------------
    Menu1 Menu2
    ----------------------------------------------
    Logo           |
                   |      
    ----------------
    Title          |
      Sub menu     |
                   |
                   |
                   | 
      """)

menu_name = input("5. Enter menu name: ").capitalize()
print(">> Set menu name {}".format(menu_name))
menu_title = input("6. Menu title: ").capitalize()
print(">> Set menu name {}".format(menu_title))
sub_menu = input("7. Submenu name: ").capitalize()
print(">> Set menu name {}".format(sub_menu))
class_name = input("8. Class name: ")


if " " in class_name:
    class_name = class_name.replace(" ", "_")

model_name = class_name
if "_" in class_name or " " in class_name:
    model_name = class_name.replace("_", ".")

print(">> Set model '{}' with one name field".format(model_name))
print(">> Set Class '{}' with one name field".format(class_name))

#create module files
#__init__.py
file_name = module_name
if " " in module_name:
    file_name = module_name.replace(" ", "_")
    
init_file = "__init__.py"
init_file_content = "import {}".format(file_name)
file = open(os.path.join(path, init_file), 'w+')
file.write(init_file_content)
file.close()

#__openerp__.py
openerp_file = "__openerp__.py"
openerp_file_content = {
	'name': module_name,
	'version': '1.0',
	'description': module_desc,
	'author': module_author,
	'website': "http://example.com",
	'depends': ['base'],
	'data': ['{}_view.xml'.format(file_name),'{}_report_view.xml'.format(module_name)],
	'demo': [],
	'installable': True,
	'auto_install': False,
}

file = open(os.path.join(path, openerp_file), 'w+')
openerp_file_content = str(openerp_file_content).replace('{','{\n\t')
openerp_file_content = str(openerp_file_content).replace('}','\n}')
file.write(str(openerp_file_content).replace(',',',\n\t'))
file.close()

#xml file


xml_data = {
    "menu_name": menu_name,
    "menu_title": menu_title,
    "sub_menu": sub_menu,
    "model": model_name,
}

xml_file = "{}_view.xml".format(file_name)
file = open(os.path.join(path, xml_file), 'w+')
xml_file_content = """<?xml version='1.0' encoding="utf-8"?>
<openerp>
    <data>
        <menuitem id="module_top_menu_id" name="{view[menu_name]}"/>
        <menuitem id="sub_menu_title" name="{view[menu_title]}" parent="module_top_menu_id"/>
        
        <record id="form_view_id" model="ir.ui.view">
            <field name="name">Form</field>
            <field name="model">{view[model]}</field>
            <field name="arch" type="xml">
                <form string="">
                    <sheet>
                        <group>
                            <field name="name"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>
        
        <record id="tree_view_id" model="ir.ui.view" >
            <field name="name">Tree view</field>
            <field name="model">{view[model]}</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                <tree string="">
                    <field name="name"/>
                </tree>
            </field>
        </record>
        
        
        <record id="menu_action" model="ir.actions.act_window">
            <field name="name">View Name</field>
            <field name="res_model">{view[model]}</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
            <field name="help" type="html">
                <p class="oe_view_nocontent_create">
                    Click Create to add new record
                </p>
            </field>
        </record>
        
        <menuitem id="left_menu" name="{view[sub_menu]}"
            parent="sub_menu_title" action="menu_action"
        />
    </data>
</openerp>
"""
xml_file_content = xml_file_content.format(view=xml_data)
file.write(str(xml_file_content))
#python file

python_file = "{}.py".format(file_name)
python_file_content = """from openerp.osv import fields, osv

class %s(osv.Model):
    _name = '%s'
    
    _columns = {
        'name': fields.char('Name'),
    }
    
"""


python_file_content = python_file_content % (class_name, model_name)
file = open(os.path.join(path, python_file), 'w+')
file.write(str(python_file_content))

# Report folder
report_dir = os.path.join(path,"report")

if not os.path.exists(report_dir):
	os.makedirs(report_dir)


init_py_content = "import {}_report".format(module_name)
file = open(os.path.join(report_dir, "__init__.py"), 'w+')
file.write(str(init_py_content))
file.close()

report_py_content = """from openerp.addons.report_webkit.webkit_report import webkit_report_extender
from openerp import SUPERUSER_ID
import time
from openerp.osv.osv import except_osv


from datetime import datetime

@webkit_report_extender("%s.form_view_id")
def extend_demo(pool, cr, uid, localcontext, context):
        
    localcontext.update({
        "time": "today"    
    })
    """
report_py_content = report_py_content % module_name
file = open(os.path.join(report_dir, dir_name+"_report.py"), 'w+')
file.write(str(report_py_content))
file.close()


report_xml_content = """<?xml version="1.0" encoding="utf-8"?>
<openerp>
    <data>
        <report auto="False"
                header="False"
                id="{model}_view_report"
                model="{model}" name="{model}"
                file="{model}/report/{model}_report.mako"
                string="Report"
                report_type="webkit"/>
    </data>
</openerp>"""

report_xml_content = report_xml_content.format(model=model_name)
file = open(os.path.join(report_dir, dir_name+"_report_view.xml"), 'w+')
file.write(str(report_xml_content))
file.close()


report_mako_content = """{<html>
    % for o in objects:
        ${o.name}
        ${time}
    % endfor
</html>
}"""

file = open(os.path.join(report_dir, dir_name+"_report.mako"), 'w+')
file.write(str(report_mako_content))
file.close()



print('-'*43)
print("Module successfully created!")
print('-'*43)
input("Press Enter to exit....")
 







