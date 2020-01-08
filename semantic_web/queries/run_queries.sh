mkdir -p ./logs
arq --data ../GameOntologyPopulated.owl --query ./1.rq --time --repeat=5 > ./logs/1.log 2>&1
arq --data ../GameOntologyPopulated.owl --query ./2.rq --time --repeat=5 > ./logs/2.log 2>&1
arq --data ../GameOntologyPopulated.owl --query ./3.rq --time --repeat=5 > ./logs/3.log 2>&1
arq --data ../GameOntologyPopulated.owl --query ./4.rq --time --repeat=5 > ./logs/4.log 2>&1
arq --data ../GameOntologyPopulated.owl --query ./5.rq --time --repeat=5 > ./logs/5.log 2>&1
arq --data ../GameOntologyPopulated.owl --query ./6.rq --time --repeat=5 > ./logs/6.log 2>&1
arq --data ../GameOntologyPopulated.owl --query ./7.rq --time --repeat=5 > ./logs/7.log 2>&1
arq --data ../GameOntologyPopulated.owl --query ./8.rq --time --repeat=5 > ./logs/8.log 2>&1
arq --data ../GameOntologyPopulated.owl --query ./9.rq --time --repeat=5 > ./logs/9.log 2>&1
