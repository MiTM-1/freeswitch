from pathlib import Path

path = Path('src/mod/endpoints/mod_sofia/sofia.c')
text = path.read_text()

replacements = [
    (
        'if (exten && (br_a = switch_channel_get_partner_uuid(channel_a))) {',
        'if ((br_a = switch_channel_get_partner_uuid(channel_a))) {'
    ),
    (
        'switch_core_session_get_uuid(session), rep, exten, (char *) refer_to->r_url->url_host, br_a);',
        'switch_core_session_get_uuid(session), rep, switch_str_nil(exten), (char *) refer_to->r_url->url_host, br_a);'
    ),
    (
        'switch_event_add_header_string(xml_params, SWITCH_STACK_BOTTOM, "refer-to-user", refer_to->r_url->url_user);',
        'switch_event_add_header_string(xml_params, SWITCH_STACK_BOTTOM, "refer-to-user", switch_str_nil(refer_to->r_url->url_user));'
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'Expected one occurrence, found {count}: {old}')
    text = text.replace(old, new, 1)

old = '''if (zstr(exten)) {\n\t\t\t\t\t\t\texten = switch_core_session_sprintf(session, "sofia/%s/sip:%s@%s%s%s",\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tprofile->name, refer_to->r_url->url_user,\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\trefer_to->r_url->url_host, port ? ":" : "", port ? port : "");\n\t\t\t\t\t\t}'''
new = '''if (zstr(exten)) {\n\t\t\t\t\t\t\tif (zstr(refer_to->r_url->url_user)) {\n\t\t\t\t\t\t\t\texten = switch_core_session_sprintf(session, "sofia/%s/sip:%s%s%s",\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tprofile->name, refer_to->r_url->url_host,\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tport ? ":" : "", port ? port : "");\n\t\t\t\t\t\t\t} else {\n\t\t\t\t\t\t\t\texten = switch_core_session_sprintf(session, "sofia/%s/sip:%s@%s%s%s",\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tprofile->name, refer_to->r_url->url_user,\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\trefer_to->r_url->url_host, port ? ":" : "", port ? port : "");\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t}'''
count = text.count(old)
if count != 1:
    raise SystemExit(f'Expected one fallback block, found {count}')
text = text.replace(old, new, 1)
path.write_text(text)
print('Issue #592 source fix applied successfully.')
