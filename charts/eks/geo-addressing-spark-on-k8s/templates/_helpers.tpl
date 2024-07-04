{{/*
Expand the name of the chart.
*/}}
{{- define "geo-addressing-spark-eks.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "geo-addressing-spark-eks.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "geo-addressing-spark-eks.labels" -}}
helm.sh/chart: {{ include "geo-addressing-spark-eks.chart" . }}
{{ include "geo-addressing-spark-eks.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "geo-addressing-spark-eks.selectorLabels" -}}
app.kubernetes.io/name: {{ include "geo-addressing-spark-eks.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "geo-addressing-spark-nfs-storage-class.name" -}}
{{- printf "%s-%s-%s" "nfs-sc" .Release.Name  .Release.Namespace | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "geo-addressing-spark-nfs-pv.name" -}}
{{- printf "%s-pv-%s-%s" "exp-snap" .Release.Name  .Release.Namespace | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "geo-addressing-spark-nfs-pvc.name" -}}
{{- printf "%s-pvc-%s-%s" "exp-snap" .Release.Name  .Release.Namespace | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Hook Storage Class
*/}}
{{- define "geo-addressing-spark-hook-storage-class.name" -}}
{{- printf "%s-%s" "hook-efs" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Hook Persistent Volume Name
*/}}
{{- define "geo-addressing-spark-hook-pv.name" -}}
{{- printf "%s-%s-%s" "hook" .Release.Name "pv" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Hook Persistent Volume Claim Name
*/}}
{{- define "geo-addressing-spark-hook-pvc.name" -}}
{{- printf "%s-%s-%s" "hook" .Release.Name "pvc" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Hook PV labels
*/}}
{{- define "geo-addressing-spark-hook-pv.labels" -}}
app.kubernetes.io/name: {{ include "geo-addressing-spark-hook-pv.name" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Hook PVC labels
*/}}
{{- define "geo-addressing-spark-hook-pvc.labels" -}}
app.kubernetes.io/name: {{ include "geo-addressing-spark-hook-pvc.name" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}