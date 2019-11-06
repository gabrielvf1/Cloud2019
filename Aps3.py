import boto3
import os


acessKey = os.environ["acessKeyCloud"]
secretAcessKey = os.environ["acessSecretKeyCloud"]

ec2 = boto3.client('ec2',region_name='us-east-1', aws_access_key_id = acessKey ,aws_secret_access_key=secretAcessKey)
chave = ec2.delete_key_pair(KeyName='Gabriel_Projeto')
chave = ec2.create_key_pair(KeyName='Gabriel_Projeto')

# print(len(ec2.describe_instances()['Reservations']))
# print(ec2.describe_instances()['Reservations'][1]['Instances'][0]['Tags'][0]['Value'])
# print(ec2.describe_instances()['Reservations'][1]['Instances'][0]['State']['Name'])
# print(ec2.describe_instances()['Reservations'][1]['Instances'][0]['SecurityGroups'][0]['GroupId'])
for i in range(len(ec2.describe_instances()['Reservations'])):
    try:
        nome = ec2.describe_instances()['Reservations'][i]['Instances'][0]['Tags'][0]['Value']
        estado = (ec2.describe_instances()['Reservations'][i]['Instances'][0]['State']['Name'])
        # print(ec2.describe_instances()['Reservations'][i]['Instances'][0]['Tags'][0]['Value'])
        # print(ec2.describe_instances()['Reservations'][i]['Instances'][0]['State']['Name'])
    except:
        nome = "Sem Nome"
        estado = (ec2.describe_instances()['Reservations'][i]['Instances'][0]['State']['Name'])
        print("Maquina sem Tag \n")
        pass
    if ((nome == 'Gabriel Francato' or nome == 'GabrielAps') and str(estado) != "terminated"):
        print("Maquina ja existe, deletando")
        lista = []
        security_group_id = ec2.describe_instances()['Reservations'][i]['Instances'][0]['SecurityGroups'][0]['GroupId']
        lista.append(ec2.describe_instances()['Reservations'][i]['Instances'][0]['InstanceId'])
        ec2.terminate_instances(InstanceIds=lista)

# print(ec2.describe_instances()['Reservations'][0]['Instances'][0]['Tags'])
# print(ec2.describe_instances())

os.chmod("/home/gabrielvf/.ssh/privada_projeto.pem", 0o777)
with open("/home/gabrielvf/.ssh/privada_projeto.pem", 'w+') as file:
    file.write(chave['KeyMaterial'])
os.chmod("/home/gabrielvf/.ssh/privada_projeto.pem", 0o400)


response = ec2.describe_vpcs()
try:
    response2 = ec2.delete_security_group(GroupName='GabrielAPS')
    print('Security Group Deleted')
    print("Security Group Nao existia, criando um novo")
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
    response = ec2.create_security_group(GroupName='GabrielAPS',Description='Teste para o Projeto',VpcId=vpc_id)
    security_group_id = response['GroupId']
    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
    data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 5000,
                'ToPort': 5000,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
    # print('Ingress Successfully Set %s' % data)

except Exception as e:
    if ((str(e)[-22:-1]) == "has a dependent objec"):
        print("Ja existe o Security Group por algum motivo nao foi possivel deletar, vamos utilizar o mesmo portanto.")
        pass
    else:
        print("Security Group Nao existia, criando um novo")
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
        response = ec2.create_security_group(GroupName='GabrielAPS',Description='Teste para o Projeto',VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                    'FromPort': 5000,
                    'ToPort': 5000,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])
        # print('Ingress Successfully Set %s' % data)
        pass

instancia = ec2.run_instances(ImageId='ami-04b9e92b5572fa0d1', MinCount=1, MaxCount=1,  InstanceType='t2.micro', KeyName='Gabriel_Projeto', SecurityGroupIds=[security_group_id,])

response = ec2.create_tags(
    Resources=[
        instancia['Instances'][0]['InstanceId'],
    ],
    Tags=[
        {
            'Key': 'Name',
            'Value': 'GabrielAps'
        },
        {
            'Key': 'Owner',
            'Value': 'Gabriel Francato'
        }
    ]
)