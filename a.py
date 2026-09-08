from pathlib import Path
import subprocess

path = Path('src/mod/endpoints/mod_sofia/sofia.c')
text = path.read_text()
replacements = [
    ('if (exten && (br_a = switch_channel_get_partner_uuid(channel_a))) {', 'if ((br_a = switch_channel_get_partner_uuid(channel_a))) {'),
    ('switch_core_session_get_uuid(session), rep, exten, (char *) refer_to->r_url->url_host, br_a);', 'switch_core_session_get_uuid(session), rep, switch_str_nil(exten), (char *) refer_to->r_url->url_host, br_a);'),
    ('switch_event_add_header_string(xml_params, SWITCH_STACK_BOTTOM, "refer-to-user", refer_to->r_url->url_user);', 'switch_event_add_header_string(xml_params, SWITCH_STACK_BOTTOM, "refer-to-user", switch_str_nil(refer_to->r_url->url_user));')
]
for old, new in replacements:
    if text.count(old) != 1:
        raise SystemExit(f'Unexpected occurrence count for: {old}')
    text = text.replace(old, new, 1)
old = '''if (zstr(exten)) {\n\t\t\t\t\t\t\texten = switch_core_session_sprintf(session, "sofia/%s/sip:%s@%s%s%s",\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tprofile->name, refer_to->r_url->url_user,\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\trefer_to->r_url->url_host, port ? ":" : "", port ? port : "");\n\t\t\t\t\t\t}'''
new = '''if (zstr(exten)) {\n\t\t\t\t\t\t\tif (zstr(refer_to->r_url->url_user)) {\n\t\t\t\t\t\t\t\texten = switch_core_session_sprintf(session, "sofia/%s/sip:%s%s%s",\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tprofile->name, refer_to->r_url->url_host,\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tport ? ":" : "", port ? port : "");\n\t\t\t\t\t\t\t} else {\n\t\t\t\t\t\t\t\texten = switch_core_session_sprintf(session, "sofia/%s/sip:%s@%s%s%s",\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tprofile->name, refer_to->r_url->url_user,\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\trefer_to->r_url->url_host, port ? ":" : "", port ? port : "");\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t}'''
if text.count(old) != 1:
    raise SystemExit('Unexpected fallback block count')
text = text.replace(old, new, 1)
path.write_text(text)
for helper in ('apply_issue_592.py', 'a.py'):
    p = Path(helper)
    if p.exists():
        p.unlink()
subprocess.run(['git','add','-A'], check=True)
subprocess.run(['git','commit','-m','fix(mod_sofia): process host-only REFER targets'], check=True)
subprocess.run(['git','push','origin','fix/issue-592-host-only-refer'], check=True)
print('DONE')
