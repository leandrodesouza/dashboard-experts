from flask import Blueprint, jsonify, request
from flask_login import login_required
from src.models.demanda import Demanda, db
from datetime import datetime, timedelta
from sqlalchemy import and_
from src.models.professor import Professor


dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/demandas', methods=['GET'])
@login_required
def get_demandas():
    # Parâmetros de filtro
    filtro_periodo = request.args.get('periodo', 'todos')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    query = Demanda.query
    
    # Aplicar filtros de período
    if filtro_periodo == 'ultimos_7_dias':
        data_limite = datetime.now().date() - timedelta(days=7)
        query = query.filter(Demanda.data_envio >= data_limite)
    elif filtro_periodo == 'mes_atual':
        hoje = datetime.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        query = query.filter(Demanda.data_envio >= primeiro_dia_mes)
    elif filtro_periodo == 'personalizado' and data_inicio and data_fim:
        data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
        query = query.filter(and_(
            Demanda.data_envio >= data_inicio_obj,
            Demanda.data_envio <= data_fim_obj
        ))
    
    # Realiza o join com Professor para trazer nome e disciplina
        resultados = db.session.query(
            Demanda,
            Professor.nome.label('professor_nome'),
            Professor.disciplina.label('professor_disciplina')
        ).join(Professor, Demanda.professor_id == Professor.id)\
        .filter(query._criterion if hasattr(query, '_criterion') else True)\
        .all()

        # Monta o JSON customizado
        lista = []
        for demanda, professor_nome, professor_disciplina in resultados:
            d = {
            'id': demanda.id,
            'professor': f"{professor_nome} – {professor_disciplina or ''}",
            'tipo_conteudo': demanda.tipo_conteudo,
            'data_envio': demanda.data_envio.strftime('%d/%m/%Y') if demanda.data_envio else '',
            'prazo_entrega': demanda.prazo_entrega.strftime('%d/%m/%Y') if demanda.prazo_entrega else '',
            'material_entregue': demanda.material_entregue or 'Pendente',
            'alcance_professor': demanda.alcance_professor or 0,
            'curtidas_professor': demanda.curtidas_professor or 0,
            'comentarios_professor': demanda.comentarios_professor or 0,
            }
            lista.append(d)
        return jsonify(lista)



   # return jsonify([demanda.to_dict() for demanda in demandas])

@dashboard_bp.route('/demandas', methods=['POST'])
@login_required
def create_demanda():
    data = request.json
    demanda = Demanda(
        professor=data['professor'],
        disciplina=data.get('disciplina', ''),
        tipo_conteudo=data['tipo_conteudo'],
        data_envio=datetime.now().date(),
        prazo_entrega=datetime.strptime(data['prazo_entrega'], '%Y-%m-%d').date()
    )
    db.session.add(demanda)
    db.session.commit()
    return jsonify(demanda.to_dict()), 201

@dashboard_bp.route('/demandas/<int:demanda_id>', methods=['PUT'])
@login_required
def update_demanda(demanda_id):
    demanda = Demanda.query.get_or_404(demanda_id)
    data = request.json
    
    # Atualizar campos de resultado
    if 'material_entregue' in data:
        demanda.material_entregue = data['material_entregue']
    if 'data_entrega' in data:
        demanda.data_entrega = datetime.strptime(data['data_entrega'], '%Y-%m-%d').date()
    if 'conformidade_roteiro' in data:
        demanda.conformidade_roteiro = data['conformidade_roteiro']
    if 'plataforma_publicacao' in data:
        demanda.plataforma_publicacao = data['plataforma_publicacao']
    if 'alcance_professor' in data:
        demanda.alcance_professor = data['alcance_professor']
    if 'impressoes_professor' in data:
        demanda.impressoes_professor = data['impressoes_professor']
    if 'curtidas_professor' in data:
        demanda.curtidas_professor = data['curtidas_professor']
    if 'comentarios_professor' in data:
        demanda.comentarios_professor = data['comentarios_professor']
    if 'compartilhamentos_professor' in data:
        demanda.compartilhamentos_professor = data['compartilhamentos_professor']
    if 'salvos_professor' in data:
        demanda.salvos_professor = data['salvos_professor']
    if 'visualizacoes_professor' in data:
        demanda.visualizacoes_professor = data['visualizacoes_professor']
    
    db.session.commit()
    return jsonify(demanda.to_dict())

@dashboard_bp.route('/demandas/<int:demanda_id>', methods=['DELETE'])
@login_required
def delete_demanda(demanda_id):
    demanda = Demanda.query.get_or_404(demanda_id)
    db.session.delete(demanda)
    db.session.commit()
    return '', 204

@dashboard_bp.route('/estatisticas', methods=['GET'])
@login_required
def get_estatisticas():
    # Parâmetros de filtro
    filtro_periodo = request.args.get('periodo', 'todos')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    query = Demanda.query
    
    # Aplicar filtros de período
    if filtro_periodo == 'ultimos_7_dias':
        data_limite = datetime.now().date() - timedelta(days=7)
        query = query.filter(Demanda.data_envio >= data_limite)
    elif filtro_periodo == 'mes_atual':
        hoje = datetime.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        query = query.filter(Demanda.data_envio >= primeiro_dia_mes)
    elif filtro_periodo == 'personalizado' and data_inicio and data_fim:
        data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
        query = query.filter(and_(
            Demanda.data_envio >= data_inicio_obj,
            Demanda.data_envio <= data_fim_obj
        ))
    
    demandas = query.all()
    
    total_demandas = len(demandas)
    materiais_entregues = len([d for d in demandas if d.material_entregue == 'Sim'])
    alcance_total = sum([d.alcance_professor or 0 for d in demandas])
    curtidas_total = sum([d.curtidas_professor or 0 for d in demandas])
    comentarios_total = sum([d.comentarios_professor or 0 for d in demandas])
    
    engajamento_medio = 0
    if alcance_total > 0:
        engajamento_medio = ((curtidas_total + comentarios_total) / alcance_total) * 100
    
    return jsonify({
        'total_demandas': total_demandas,
        'materiais_entregues': materiais_entregues,
        'alcance_total': alcance_total,
        'engajamento_medio': round(engajamento_medio, 1)
    })

@dashboard_bp.route('/professores/estatisticas', methods=['GET'])
@login_required
def get_estatisticas_professores():
    # Parâmetros de filtro
    filtro_periodo = request.args.get('periodo', 'todos')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    query = Demanda.query
    
    # Aplicar filtros de período
    if filtro_periodo == 'ultimos_7_dias':
        data_limite = datetime.now().date() - timedelta(days=7)
        query = query.filter(Demanda.data_envio >= data_limite)
    elif filtro_periodo == 'mes_atual':
        hoje = datetime.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        query = query.filter(Demanda.data_envio >= primeiro_dia_mes)
    elif filtro_periodo == 'personalizado' and data_inicio and data_fim:
        data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
        query = query.filter(and_(
            Demanda.data_envio >= data_inicio_obj,
            Demanda.data_envio <= data_fim_obj
        ))
    
    demandas = query.all()
    professores_stats = {}
    
    professores = [
        'Pedro Campos', 'Pablo', 'Rafael Araújo', 'Samuel', 'Tiago Vidal',
        'Rogério Dalvipa', 'Lucas Fávero', 'Pedro Canezin', 'Filipe Ávila',
        'João Paulo', 'Heitor'
    ]
    
    for professor in professores:
        demandas_prof = [d for d in demandas if d.professor == professor]
        entregues_prof = [d for d in demandas_prof if d.material_entregue == 'Sim']
        
        professores_stats[professor] = {
            'demandas': len(demandas_prof),
            'entregues': len(entregues_prof),
            'alcance_total': sum([d.alcance_professor or 0 for d in demandas_prof]),
            'curtidas_total': sum([d.curtidas_professor or 0 for d in demandas_prof])
        }
    
    return jsonify(professores_stats)



import csv
import io
from flask import make_response
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

@dashboard_bp.route('/exportar/csv', methods=['GET'])
@login_required
def exportar_csv():
    # Parâmetros de filtro
    filtro_periodo = request.args.get('periodo', 'todos')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    query = Demanda.query
    
    # Aplicar filtros de período
    if filtro_periodo == 'ultimos_7_dias':
        data_limite = datetime.now().date() - timedelta(days=7)
        query = query.filter(Demanda.data_envio >= data_limite)
    elif filtro_periodo == 'mes_atual':
        hoje = datetime.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        query = query.filter(Demanda.data_envio >= primeiro_dia_mes)
    elif filtro_periodo == 'personalizado' and data_inicio and data_fim:
        data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
        query = query.filter(and_(
            Demanda.data_envio >= data_inicio_obj,
            Demanda.data_envio <= data_fim_obj
        ))
    
    demandas = query.all()
    
    # Criar CSV em memória
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Cabeçalhos
    headers = [
        'ID', 'Professor', 'Disciplina', 'Tipo de Conteúdo', 'Data Envio', 
        'Prazo Entrega', 'Material Entregue', 'Data Entrega', 'Conformidade',
        'Plataforma', 'Alcance', 'Impressões', 'Curtidas', 'Comentários',
        'Compartilhamentos', 'Salvos', 'Visualizações'
    ]
    writer.writerow(headers)
    
    # Dados
    for demanda in demandas:
        row = [
            f'DEM{str(demanda.id).zfill(3)}',
            demanda.professor,
            demanda.disciplina or '',
            demanda.tipo_conteudo,
            demanda.data_envio.strftime('%d/%m/%Y') if demanda.data_envio else '',
            demanda.prazo_entrega.strftime('%d/%m/%Y') if demanda.prazo_entrega else '',
            demanda.material_entregue or 'Pendente',
            demanda.data_entrega.strftime('%d/%m/%Y') if demanda.data_entrega else '',
            demanda.conformidade_roteiro or '',
            demanda.plataforma_publicacao or '',
            demanda.alcance_professor or 0,
            demanda.impressoes_professor or 0,
            demanda.curtidas_professor or 0,
            demanda.comentarios_professor or 0,
            demanda.compartilhamentos_professor or 0,
            demanda.salvos_professor or 0,
            demanda.visualizacoes_professor or 0
        ]
        writer.writerow(row)
    
    # Preparar resposta
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=dashboard_experts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response

@dashboard_bp.route('/exportar/pdf', methods=['GET'])
@login_required
def exportar_pdf():
    # Parâmetros de filtro
    filtro_periodo = request.args.get('periodo', 'todos')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    query = Demanda.query
    
    # Aplicar filtros de período
    if filtro_periodo == 'ultimos_7_dias':
        data_limite = datetime.now().date() - timedelta(days=7)
        query = query.filter(Demanda.data_envio >= data_limite)
    elif filtro_periodo == 'mes_atual':
        hoje = datetime.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        query = query.filter(Demanda.data_envio >= primeiro_dia_mes)
    elif filtro_periodo == 'personalizado' and data_inicio and data_fim:
        data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
        query = query.filter(and_(
            Demanda.data_envio >= data_inicio_obj,
            Demanda.data_envio <= data_fim_obj
        ))
    
    demandas = query.all()
    
    # Criar PDF em memória
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Centralizado
    )
    
    # Elementos do documento
    elements = []
    
    # Título
    title = Paragraph("Dashboard Projeto Experts - Relatório de Demandas", title_style)
    elements.append(title)
    
    # Informações do filtro
    periodo_texto = {
        'todos': 'Todos os períodos',
        'ultimos_7_dias': 'Últimos 7 dias',
        'mes_atual': 'Mês atual',
        'personalizado': f'Período personalizado ({data_inicio} a {data_fim})' if data_inicio and data_fim else 'Período personalizado'
    }
    
    info_filtro = Paragraph(f"<b>Período:</b> {periodo_texto.get(filtro_periodo, 'Todos os períodos')}", styles['Normal'])
    elements.append(info_filtro)
    elements.append(Spacer(1, 12))
    
    # Estatísticas resumidas
    total_demandas = len(demandas)
    materiais_entregues = len([d for d in demandas if d.material_entregue == 'Sim'])
    alcance_total = sum([d.alcance_professor or 0 for d in demandas])
    
    stats_data = [
        ['Métrica', 'Valor'],
        ['Total de Demandas', str(total_demandas)],
        ['Materiais Entregues', f'{materiais_entregues}/{total_demandas}'],
        ['Alcance Total', f'{alcance_total:,}']
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 20))
    
    # Tabela de demandas
    if demandas:
        demandas_title = Paragraph("Detalhamento das Demandas", styles['Heading2'])
        elements.append(demandas_title)
        elements.append(Spacer(1, 12))
        
        # Cabeçalhos da tabela
        table_data = [
            ['ID', 'Professor', 'Tipo', 'Data Envio', 'Status', 'Alcance', 'Curtidas']
        ]
        
        # Dados das demandas
        for demanda in demandas:
            row = [
                f'DEM{str(demanda.id).zfill(3)}',
                demanda.professor[:15] + '...' if len(demanda.professor) > 15 else demanda.professor,
                demanda.tipo_conteudo[:10] + '...' if len(demanda.tipo_conteudo) > 10 else demanda.tipo_conteudo,
                demanda.data_envio.strftime('%d/%m/%Y') if demanda.data_envio else '',
                demanda.material_entregue or 'Pendente',
                str(demanda.alcance_professor or 0),
                str(demanda.curtidas_professor or 0)
            ]
            table_data.append(row)
        
        # Criar tabela
        demandas_table = Table(table_data, colWidths=[0.8*inch, 1.5*inch, 1*inch, 1*inch, 1*inch, 0.8*inch, 0.8*inch])
        demandas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        elements.append(demandas_table)
    else:
        no_data = Paragraph("Nenhuma demanda encontrada para o período selecionado.", styles['Normal'])
        elements.append(no_data)
    
    # Rodapé
    elements.append(Spacer(1, 30))
    footer = Paragraph(f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}", styles['Normal'])
    elements.append(footer)
    
    # Construir PDF
    doc.build(elements)
    
    # Preparar resposta
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=dashboard_experts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    
    return response

