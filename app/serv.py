from meinheld import server

from cykor_memo.wsgi import application

server.listen(("0.0.0.0", 8000))
server.run(application)
