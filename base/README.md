## Justificativa da implementação

1. **Por que as rotas de autenticação foram movidas para `auth.py`?**  
   As rotas de autenticação (`/registro`, `/login`, `/logout`) ficaram no blueprint `auth_bp` para separar responsabilidades: `auth.py` concentra login/cadastro/logout, enquanto `app.py` mantém apenas o CRUD de treinos.

2. **Como a aplicação identifica o usuário logado usando `session`?**  
   Após login certo, o código salva `session['usuario_id']` e `session['nome']`. As rotas com segurança de login verificam `session['usuario_id']` e se não existir, redirecionam para `auth.login`.

3. **Como o código impede que um usuário acesse treinos de outro usuário?**  
   A listagem da home usa `listar_treinos(session['usuario_id'])`, exibindo só treinos do dono logado. Além disso, antes de editar/concluir/excluir, o treino é buscado no banco e seu `usuario_id` é comparado com `session['usuario_id']` e quando é igual, a resposta é `403`.
