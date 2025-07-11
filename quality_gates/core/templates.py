from quality_gates.schemas import Comment

def jira_template(info: Comment):
    jira_comment = f"""\
    Разворачивание сервиса {info.service_name} 
    с версией {info.version} развернуто
    Исполнитель: {info.executor}
    CI/CD под запросом на разворачивание сервиса: {info.pipeline_url}
    
    Комментарий оставлен средством автоматизации Quality Gates
    """
    return str(jira_comment)