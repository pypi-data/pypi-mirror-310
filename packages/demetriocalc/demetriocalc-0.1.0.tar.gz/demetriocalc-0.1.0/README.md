# Estrutura do Código

A classe **Calculadora** contém os seguintes métodos:

- `soma(a, b)`: Retorna a soma de `a` e `b`.
- `subtracao(a, b)`: Retorna a diferença entre `a` e `b`.
- `multiplicacao(a, b)`: Retorna o produto de `a` e `b`.
- `divisao(a, b)`: Retorna o resultado da divisão de `a` por `b`. Caso o divisor `b` seja zero, uma mensagem de erro é retornada indicando que a divisão por zero não é permitida.

**Parâmetros:**

- `a`: Primeiro número (int ou float).
- `b`: Segundo número (int ou float).

---

## Exemplo de Uso

```python
from demetriocalc import Calculadora

calc = Calculadora()
print(calc.soma(5, 3))          # Saída: 8
print(calc.subtracao(5, 3))     # Saída: 2
print(calc.multiplicacao(5, 3)) # Saída: 15
print(calc.divisao(5, 0))       # Saída: "Erro: Divisão por zero não é permitida"
