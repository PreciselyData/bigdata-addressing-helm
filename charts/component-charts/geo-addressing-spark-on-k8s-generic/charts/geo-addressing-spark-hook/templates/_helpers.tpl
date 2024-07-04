{{/*
Expand the name of the chart.
*/}}
{{- define "geo-addressing-spark-hook.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "geo-addressing-spark-hook.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "geo-addressing-spark-hook.labels" -}}
helm.sh/chart: {{ include "geo-addressing-spark-hook.chart" . }}
{{ include "geo-addressing-spark-hook.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "geo-addressing-spark-hook.selectorLabels" -}}
app.kubernetes.io/name: {{ include "geo-addressing-spark-hook.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}


{{/*
volumeMounts
*/}}
{{- define "geo-addressing-spark-hook.volumeMounts" -}}
- name: geo-addressing-spark-host-volume
  mountPath: {{ .Values.global.nfs.volumeMountPath }}
{{- end }}
