param (
    [string]$Server,
    [string]$User,
    [string]$Token
)

docker login $Server --username $User --password $Token --tls-verify=false
