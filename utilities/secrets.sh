ProjectName="--- project name ---" 
TenantName="--- tenant name ---" 
EnvironmentName="--- environment name ---" 
ComponentName="risk"
AWS_REGION="us-east-1" 
riskAPIKey="---risk api key ---"

if aws ssm put-parameter --region ${AWS_REGION} --name "${ProjectName}-${TenantName}-${EnvironmentName}-${ComponentName}-apikey" --type "SecureString" --value "${riskAPIKey}" --tier Standard --overwrite; then
        echo "risk APIKey ssm put parameter complete"
fi
