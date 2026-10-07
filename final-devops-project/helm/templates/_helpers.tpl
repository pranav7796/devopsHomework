{{- define "homework-api.name" -}}{{ .Chart.Name }}{{- end -}}
{{- define "homework-api.labels" -}}
app.kubernetes.io/name: {{ include "homework-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
