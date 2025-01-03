import pandas as pd
import numpy as np
import streamlit as st

class MegaSena:
    def __init__(self, numeros, linhas=1, n_sequencia=3):
        # Armazena os números das primeiras linhas especificadas
        self.numeros = numeros.head(linhas)
        self.n_sequencia = n_sequencia
    
    def inversao(self):
        # Inverte os dígitos de cada número em todas as colunas
        self.inversoes = pd.concat([(self.numeros
                                     .applymap(lambda x: int(str(x)[::-1]) if isinstance(x, int) 
                                               else x)
                                     .stack()), 
                                    self.numeros.stack()]).reset_index(drop=True)
    
        
        return self.inversoes 

    def sequencia (self):
        min = 0 - self.n_sequencia
        max = 1 + self.n_sequencia
        self.sequencias = self.inversoes.apply(lambda x: [x+i for i in range(min,max)]).explode().reset_index(drop=True)
        return self.sequencias

    def pontuação(self):
        # Calcula a contagem das sequências
        contagem = self.sequencias.value_counts()
        
        # Calcula a normalização Min-Max
        min_freq = contagem.min()
        max_freq = contagem.max()
        normalizacao_min_max = (contagem - min_freq) / (max_freq - min_freq)
        
        # Concatena as informações em um DataFrame
        self.pontuacao = (
            pd.concat([contagem, normalizacao_min_max], axis=1)
            .reset_index()
            .rename(columns={'index': 'numero', 0: 'contagem', 1: 'normalizado'})
            .drop_duplicates()
        )
        
        return self.pontuacao

def main():
    global uploaded_file, linhas, sequencia
    st.title('Calculadora de Números por Numerologia')

    st.header('Upload do Arquivo')
    uploaded_file = st.file_uploader('Seleciona um Arquivo', type=['xlsx','csv'])


    st.header('Definindo o Parâmetros')
    linhas = st.slider('Escolha o Número de Sorteios', 0, 50, 5)
    sequencia = st.slider('Escolha o Tamanho das sequencias de números', 0, 10, 2)

def processamento():
    global df,resultado
    df = (pd.read_excel(uploaded_file, header=0)
            .sort_values('Concurso', ascending=False)
            .filter(like='Bola')
           )
    
    processamento = MegaSena(df, linhas=linhas, n_sequencia=sequencia)
    processamento.inversao()
    processamento.sequencia()

    resultado = processamento.pontuação()
    resultado = resultado.loc[(resultado.numero > 0) & (resultado.numero <=60)]

def resultados():
    st.header('Sorteios Selecionados')
    st.dataframe(df.head(linhas))
    st.header('Resultados da Análise dos Números')
    possiveis_numeros = resultado.numero.sort_values().unique()
    #st.markdown(possiveis_numeros)
    
    numeros_selecionados = st.slider('Seleção de Números', 1, len(possiveis_numeros), 10 )
    st.dataframe(resultado)



main()
processamento()
resultados()