{{/*
Expand the name of the chart.
*/}}
{{- define "geo-addressing-spark-helm.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "geo-addressing-spark-helm.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "geo-addressing-spark-helm.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "geo-addressing-spark-helm.labels" -}}
helm.sh/chart: {{ include "geo-addressing-spark-helm.chart" . }}
{{ include "geo-addressing-spark-helm.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "geo-addressing-spark-helm.selectorLabels" -}}
app.kubernetes.io/name: {{ include "geo-addressing-spark-helm.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "geo-addressing-spark-helm.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "geo-addressing-spark-helm.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "geo-addressing-spark-cluster-role-binding.name" -}}
{{- printf "%s-%s-%s" "role-binding" .Release.Name  .Release.Namespace | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "geo-addressing-spark-secret.name" -}}
{{- printf "%s-%s-%s" "secret" .Release.Name  .Release.Namespace | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "geo-addressing-spark-application.name" -}}
{{- printf "%s-%s" .Release.Name .Release.Namespace | trunc 63 | trimSuffix "-" }}
{{- end }}
