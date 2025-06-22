from services import supabase

# Teste: pegar os 5 primeiros registros da tabela 'pedidos'
response = supabase.table('pedidos').select('*').limit(5).execute()

print(response.data)  # Imprime os dados
print(response.error) # Verifica se há erro
