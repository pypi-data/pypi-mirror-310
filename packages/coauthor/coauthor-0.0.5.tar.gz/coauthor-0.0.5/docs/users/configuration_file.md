# Configuration file

The Coauthor configuration file which is default named `.coauthor.yml` can be used to configure

## Hugo Translation

The following example shows how the Coauthor AI agent can be used to support translations of Hugo websites. The configuration below if started with

```bash
coauthor --watch
```

will watch the Markdown files in directory `content/en/`. If a file is saved with `translate: true` in the frontmatter sections this will trigger the workflow tasks `ai-translate` and `write-file`. The first task will translate the content of the page and store it as an attribute of the task with key `response`. The next task will use `write_file` type task to write the response to a new file or update existing file.

```yaml
---
jinja:
  search_path: .coauthor/templates
  custom_delimiters:
    block_start_string: "{{%"
    block_end_string: "%}}"
    variable_start_string: "{{{"
    variable_end_string: "}}}"
agent:
  api_key_var: OPENAI_API_KEY
  api_url_var: OPENAI_API_URL
  model: openai/gpt-4o
workflows:
  - name: hugo-translation
    path_patterns:
      - .*\.md$
    content_patterns:
      - ".*translate: true.*"
    watch:
      filesystem:
        paths:
          - content/en/
    tasks:
      - id: ai-translate
        type: process_file_with_openai_agent
        system: |
          You are a Translator AI Agent. You receive input in English and then
          translate to Dutch.
      - id: write-file
        type: write_file
        path: >
          {{ config['current-task']['path-modify-event']
          | replace('content/en', 'content/nl') }}
        content: >-
          {{ config | get_task_attribute('ai-translate', 'response') }}
```

