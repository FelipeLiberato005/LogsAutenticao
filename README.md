Autenticação para delivery

 Este projeto visa melhorar o sistema de autenticação com o uso de IA para gerar logs de autenticação detalhados. A Inteligência Artificial será aplicada na análise desses logs para detectar anomalias e possíveis ameaças. O sistema permitirá que os administradores do app sejam alertados automaticamente em tempo real, caso haja um padrão de comportamento suspeito.
Além disso, a IA será treinada com dados históricos para aprender os comportamentos normais dos usuários e identificar, assim, padrões que indiquem tentativas de fraude, como logins múltiplos em um curto espaço de tempo, tentativas de acesso de dispositivos desconhecidos ou localizações geográficas inesperadas.

O codigo, guarda informações de logins dos usuarios tipo: O ip do usuario, para podermos saber de qual região está sendo feito o acesso, e permitir que a Ia identifique a normalidade do login(se existir três ips diferentes, algo claramente está estranho) e assim, notifique o administrador, para poder alertar o dono da conta; O usuario, para poder acessar a conta, o cliente deverá ter um nome de usuario e senha, a ideia é fazer com que a Ia identifique algum tipo de anormalidade na hora do cliente fazer login(caso o dono da conta ou não, erre no maximo 3 vezes a senha) será emitido um alerta para equipe de administrador; Horario do acesso também será guardado, por segurança; Quantos ips distindo existem naquela conta; Se a tentativa de login foi sucedida ou não; A classificação do login "Suspeito" ou "Normal". Tudo isso será guardadp em uma tabela no python e em um arquivo formato Excel



Felipe Liberato Araujo
