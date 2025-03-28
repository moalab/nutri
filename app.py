import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import math

# Set page configuration
st.set_page_config(
    page_title="Calculadora de Saúde",
    page_icon="🏥",
    layout="wide"
)

# App title and description
st.title("Calculadora de Saúde")
st.markdown("Esta aplicação calcula e visualiza métricas de saúde como IMC e relação cintura-quadril.")

# Initialize session state for saving user inputs
if 'saved_metrics' not in st.session_state:
    st.session_state.saved_metrics = []

# Create columns for a more organized layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Dados Pessoais")
    
    # Personal information inputs
    nome = st.text_input("Nome (opcional)")
    idade = st.number_input("Idade", min_value=10, max_value=100, value=30)
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
    
    # Measurements inputs
    st.subheader("Medidas Corporais")
    altura = st.number_input("Altura (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
    peso = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
    cintura = st.number_input("Circunferência da Cintura (cm)", min_value=40.0, max_value=200.0, value=80.0, step=0.1)
    quadril = st.number_input("Circunferência do Quadril (cm)", min_value=40.0, max_value=200.0, value=100.0, step=0.1)

    # Buttons for calculating, saving and resetting
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        calcular = st.button("Calcular", use_container_width=True)
    with col_btn2:
        salvar = st.button("Salvar Resultados", use_container_width=True)
    with col_btn3:
        reset = st.button("Limpar", use_container_width=True)

with col2:
    if calcular or salvar:
        st.subheader("Resultados")
        
        # Calculate BMI
        altura_m = altura / 100  # Convert height from cm to m
        imc = peso / (altura_m ** 2)
        
        # Calculate waist-to-hip ratio
        rcq = cintura / quadril
        
        # BMI categories according to WHO
        if imc < 18.5:
            imc_categoria = "Abaixo do Peso"
            imc_cor = "blue"
        elif 18.5 <= imc < 25:
            imc_categoria = "Peso Normal"
            imc_cor = "green"
        elif 25 <= imc < 30:
            imc_categoria = "Sobrepeso"
            imc_cor = "orange"
        else:
            imc_categoria = "Obesidade"
            imc_cor = "red"
        
        # RCQ (waist-to-hip ratio) risk categories
        if sexo == "Masculino":
            if rcq < 0.9:
                rcq_risco = "Baixo"
                rcq_cor = "green"
            elif 0.9 <= rcq < 1.0:
                rcq_risco = "Moderado"
                rcq_cor = "orange"
            else:
                rcq_risco = "Alto"
                rcq_cor = "red"
        else:  # Female
            if rcq < 0.8:
                rcq_risco = "Baixo"
                rcq_cor = "green"
            elif 0.8 <= rcq < 0.85:
                rcq_risco = "Moderado"
                rcq_cor = "orange"
            else:
                rcq_risco = "Alto"
                rcq_cor = "red"
        
        # Display metrics
        col_metric1, col_metric2 = st.columns(2)
        with col_metric1:
            st.metric("IMC", f"{imc:.2f} kg/m²")
            st.markdown(f"<h4 style='color:{imc_cor};'>Classificação: {imc_categoria}</h4>", unsafe_allow_html=True)
        
        with col_metric2:
            st.metric("Relação Cintura-Quadril", f"{rcq:.2f}")
            st.markdown(f"<h4 style='color:{rcq_cor};'>Risco: {rcq_risco}</h4>", unsafe_allow_html=True)
        
        # Visualizations
        st.subheader("Visualizações")
        
        # IMC gauge chart
        fig_imc = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = imc,
            title = {'text': "IMC"},
            gauge = {
                'axis': {'range': [None, 40], 'tickwidth': 1},
                'bar': {'color': imc_cor},
                'steps': [
                    {'range': [0, 18.5], 'color': 'lightblue'},
                    {'range': [18.5, 25], 'color': 'lightgreen'},
                    {'range': [25, 30], 'color': 'lightyellow'},
                    {'range': [30, 40], 'color': 'lightcoral'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': imc
                }
            }
        ))
        fig_imc.update_layout(height=300)
        st.plotly_chart(fig_imc, use_container_width=True)
        
        # RCQ gauge chart
        max_rcq = 1.2 if sexo == "Masculino" else 1.0
        fig_rcq = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = rcq,
            title = {'text': "Relação Cintura-Quadril"},
            gauge = {
                'axis': {'range': [0, max_rcq], 'tickwidth': 1},
                'bar': {'color': rcq_cor},
                'steps': [
                    {'range': [0, 0.8 if sexo == "Feminino" else 0.9], 'color': 'lightgreen'},
                    {'range': [0.8 if sexo == "Feminino" else 0.9, 
                              0.85 if sexo == "Feminino" else 1.0], 'color': 'lightyellow'},
                    {'range': [0.85 if sexo == "Feminino" else 1.0, max_rcq], 'color': 'lightcoral'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': rcq
                }
            }
        ))
        fig_rcq.update_layout(height=300)
        st.plotly_chart(fig_rcq, use_container_width=True)
        
        # Health recommendations
        st.subheader("Recomendações")
        
        # BMI recommendations
        if imc < 18.5:
            st.info("Seu IMC indica que você está abaixo do peso ideal. Considere consultar um nutricionista para avaliar sua dieta e garantir que você está recebendo todos os nutrientes necessários.")
        elif 18.5 <= imc < 25:
            st.success("Seu IMC está na faixa de peso normal. Continue mantendo hábitos saudáveis como alimentação equilibrada e atividade física regular.")
        elif 25 <= imc < 30:
            st.warning("Seu IMC indica sobrepeso. Considere aumentar sua atividade física e revisar sua alimentação para reduzir o risco de problemas de saúde.")
        else:
            st.error("Seu IMC indica obesidade. Recomenda-se procurar orientação médica e nutricional para desenvolver um plano de saúde adequado.")
        
        # RCQ recommendations
        if (sexo == "Masculino" and rcq >= 1.0) or (sexo == "Feminino" and rcq >= 0.85):
            st.error("Sua relação cintura-quadril indica alto risco para doenças cardiovasculares. Considere consultar um médico para uma avaliação completa.")
        elif (sexo == "Masculino" and rcq >= 0.9) or (sexo == "Feminino" and rcq >= 0.8):
            st.warning("Sua relação cintura-quadril indica risco moderado para doenças cardiovasculares. Atividade física regular e alimentação saudável podem ajudar a reduzir esse risco.")
        else:
            st.success("Sua relação cintura-quadril está em uma faixa saudável. Continue mantendo hábitos de vida saudáveis.")
        
        # Save metrics if requested
        if salvar:
            data_atual = pd.Timestamp.now().strftime("%d/%m/%Y %H:%M")
            
            # Create a dictionary with the metrics to save
            metric_data = {
                "Nome": nome if nome else "Anônimo",
                "Data": data_atual,
                "Idade": idade,
                "Sexo": sexo,
                "Altura (cm)": altura,
                "Peso (kg)": peso,
                "IMC": round(imc, 2),
                "Classificação IMC": imc_categoria,
                "Cintura (cm)": cintura,
                "Quadril (cm)": quadril,
                "RCQ": round(rcq, 2),
                "Risco RCQ": rcq_risco
            }
            
            # Add the metrics to the session state
            st.session_state.saved_metrics.append(metric_data)
            st.success("Resultados salvos com sucesso!")

    # If reset button is clicked, clear all inputs
    if reset:
        # This will cause the app to rerun with default values
        st.rerun()

# Show saved metrics history if any
if st.session_state.saved_metrics:
    st.subheader("Histórico de Medições")
    
    # Convert the list of dictionaries to a dataframe
    df_metrics = pd.DataFrame(st.session_state.saved_metrics)
    
    # Display the dataframe
    st.dataframe(df_metrics, use_container_width=True)
    
    # Option to clear history
    if st.button("Limpar Histórico"):
        st.session_state.saved_metrics = []
        st.rerun()
    
    # Visualize trends if there are multiple entries
    if len(st.session_state.saved_metrics) > 1:
        st.subheader("Tendências")
        
        # Create a line chart for IMC over time
        fig_trend_imc = px.line(df_metrics, x="Data", y="IMC", 
                              title="Evolução do IMC ao longo do tempo",
                              labels={"IMC": "IMC (kg/m²)", "Data": "Data da Medição"})
        st.plotly_chart(fig_trend_imc, use_container_width=True)
        
        # Create a line chart for RCQ over time
        fig_trend_rcq = px.line(df_metrics, x="Data", y="RCQ", 
                               title="Evolução da Relação Cintura-Quadril ao longo do tempo",
                               labels={"RCQ": "Relação Cintura-Quadril", "Data": "Data da Medição"})
        st.plotly_chart(fig_trend_rcq, use_container_width=True)

# Footer with additional information
st.markdown("---")
st.markdown("""
### Referências

**IMC (Índice de Massa Corporal):**
- Abaixo do Peso: < 18.5 kg/m²
- Peso Normal: 18.5 - 24.9 kg/m²
- Sobrepeso: 25 - 29.9 kg/m²
- Obesidade: ≥ 30 kg/m²

**Relação Cintura-Quadril (RCQ):**
- Homens: 
  - Baixo Risco: < 0.9
  - Risco Moderado: 0.9 - 0.99
  - Alto Risco: ≥ 1.0
- Mulheres:
  - Baixo Risco: < 0.8
  - Risco Moderado: 0.8 - 0.84
  - Alto Risco: ≥ 0.85

**Nota:** Esta calculadora é apenas para fins informativos e não substitui a consulta a um profissional de saúde.
""")
