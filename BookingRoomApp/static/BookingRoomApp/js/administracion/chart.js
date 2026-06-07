document.addEventListener('DOMContentLoaded', function() {
  console.log('=== Chart.js Loading ===');
  const data = window.estadisticasData || {};
  console.log('Data loaded:', data);
  const backgroundColor = 'rgba(209, 138, 91, 0.7)';
  
  // Función helper para crear charts de forma segura
  function crearChart(canvasId, config) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
      console.log(`Canvas ${canvasId} no encontrado`);
      return null;
    }
    
    // Destruir chart existente si hay uno
    if (canvas._chart) {
      canvas._chart.destroy();
    }
    
    // Agregar opciones para mostrar todas las etiquetas
    if (!config.options) config.options = {};
    if (!config.options.scales) config.options.scales = {};
    if (!config.options.scales.x) config.options.scales.x = {};
    if (!config.options.scales.y) config.options.scales.y = {};
    
    // Guardar las etiquetas originales para el tooltip
    let labelsOriginales = [];
    if (config.data && config.data.labels) {
      labelsOriginales = [...config.data.labels];
    }
    
    // Función para truncar etiquetas largas
    function truncateLabel(label, maxLength) {
      if (typeof label !== 'string') label = String(label);
      if (label.length > maxLength) {
        return label.substring(0, maxLength - 4) + '...';
      }
      return label;
    }
    
    // Truncar las etiquetas en los datos si existen
    if (config.data && config.data.labels) {
      config.data.labels = config.data.labels.map(label => truncateLabel(label, 15));
    }
    
    // Configurar que las etiquetas del eje X se muestren
    config.options.scales.x.ticks = {
      autoSkip: false,
      maxRotation: 0,
      minRotation: 0,
      font: { size: 10 }
    };
    
    // Agregar padding al eje X para evitar que se corten las etiquetas
    config.options.scales.x.padding = 10;
    
    // Configurar tooltips para mostrar etiqueta completa
    config.options.plugins = config.options.plugins || {};
    config.options.plugins.tooltip = {
      callbacks: {
        title: function(context) {
          const index = context[0].dataIndex;
          return labelsOriginales[index] || '';
        },
        label: function(context) {
          return context.dataset.label + ': ' + context.raw;
        }
      }
    };
    
    // Crear nuevo chart
    const chart = new Chart(canvas, config);
    canvas._chart = chart; // Guardar referencia
    return chart;
  }
  
  // ==========================================
  // TAB: EQUIPAMIENTO
  // ==========================================
  
  // Equipamiento mas requerido
  console.log('Chart 1 - Data:', data.equipamiento_requerido);
  if (data.equipamiento_requerido && data.equipamiento_requerido.length > 0) {
    crearChart('chart-equipamiento-requerido', {
      type: 'bar',
      data: {
        labels: data.equipamiento_requerido.map(item => item.nombre),
        datasets: [{
          label: 'Frecuencia',
          data: data.equipamiento_requerido.map(item => item.frecuencia),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } } 
      }
    });
  }

  // Dinero generado por equipamiento
  console.log('Chart 2 - Data:', data.equipamiento_dinero);
  if (data.equipamiento_dinero && data.equipamiento_dinero.length > 0) {
    crearChart('chart-equipamiento-dinero', {
      type: 'bar',
      data: {
        labels: data.equipamiento_dinero.map(item => item.nombre),
        datasets: [{
          label: 'Dinero Generado ($)',
          data: data.equipamiento_dinero.map(item => item.dinero_generado),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } } 
      }
    });
  }

  // Equipamiento mas usado por tipo de evento
  console.log('Chart 3 - Data:', data.equipamiento_evento);
  if (data.equipamiento_evento && data.equipamiento_evento.length > 0) {
    crearChart('chart-equipamiento-evento', {
      type: 'bar',
      data: {
        labels: data.equipamiento_evento.map(item => `${item.tipo_evento} - ${item.equipamiento}`),
        datasets: [{
          label: 'Frecuencia',
          data: data.equipamiento_evento.map(item => item.frecuencia),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // ==========================================
  // TAB: SERVICIOS
  // ==========================================
  
  // Servicios mas requeridos
  console.log('Chart 4 - Data:', data.servicios_requeridos);
  if (data.servicios_requeridos && data.servicios_requeridos.length > 0) {
    crearChart('chart-servicios-requeridos', {
      type: 'bar',
      data: {
        labels: data.servicios_requeridos.map(item => item.nombre),
        datasets: [{
          label: 'Frecuencia',
          data: data.servicios_requeridos.map(item => item.frecuencia),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } } 
      }
    });
  }

  // Dinero generado por servicios
  console.log('Chart 5 - Data:', data.servicios_dinero);
  if (data.servicios_dinero && data.servicios_dinero.length > 0) {
    crearChart('chart-servicios-dinero', {
      type: 'bar',
      data: {
        labels: data.servicios_dinero.map(item => item.nombre),
        datasets: [{
          label: 'Dinero Generado ($)',
          data: data.servicios_dinero.map(item => item.dinero_generado),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } } 
      }
    });
  }

  // Servicios mas usados por tipo de evento
  console.log('Chart 5b - Data:', data.servicios_evento);
  if (data.servicios_evento && data.servicios_evento.length > 0) {
    crearChart('chart-servicios-evento', {
      type: 'bar',
      data: {
        labels: data.servicios_evento.map(item => `${item.tipo_evento} - ${item.servicio}`),
        datasets: [{
          label: 'Frecuencia',
          data: data.servicios_evento.map(item => item.frecuencia),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // ==========================================
  // TAB: MOBILIARIO
  // ==========================================
  
  // Mobiliario mas requerido
  console.log('Chart 6 - Data:', data.mobiliario_requerido);
  if (data.mobiliario_requerido && data.mobiliario_requerido.length > 0) {
    crearChart('chart-mobiliario-requerido', {
      type: 'bar',
      data: {
        labels: data.mobiliario_requerido.map(item => item.nombre),
        datasets: [{
          label: 'Frecuencia',
          data: data.mobiliario_requerido.map(item => item.frecuencia),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } } 
      }
    });
  }

  // Dinero generado por mobiliario
  console.log('Chart 7 - Data:', data.mobiliario_dinero);
  if (data.mobiliario_dinero && data.mobiliario_dinero.length > 0) {
    crearChart('chart-mobiliario-dinero', {
      type: 'bar',
      data: {
        labels: data.mobiliario_dinero.map(item => item.nombre),
        datasets: [{
          label: 'Dinero Generado ($)',
          data: data.mobiliario_dinero.map(item => item.dinero_generado),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } } 
      }
    });
  }

  // Mobiliario mas usado por tipo de evento
  console.log('Chart 7b - Data:', data.mobiliario_evento);
  if (data.mobiliario_evento && data.mobiliario_evento.length > 0) {
    crearChart('chart-mobiliario-evento', {
      type: 'bar',
      data: {
        labels: data.mobiliario_evento.map(item => `${item.tipo_evento} - ${item.mobiliario}`),
        datasets: [{
          label: 'Frecuencia',
          data: data.mobiliario_evento.map(item => item.frecuencia),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // ==========================================
  // TAB: SALONES
  // ==========================================
  
  // Salones mas utilizados
  console.log('Chart 8 - Data:', data.salones_utilizados);
  if (data.salones_utilizados && data.salones_utilizados.length > 0) {
    crearChart('chart-salones-utilizados', {
      type: 'bar',
      data: {
        labels: data.salones_utilizados.map(item => item.nombre),
        datasets: [{
          label: 'Veces Utilizado',
          data: data.salones_utilizados.map(item => item.veces_utilizado),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } } 
      }
    });
  }

  // Dinero generado por salones
  console.log('Chart 9 - Data:', data.salones_dinero);
  if (data.salones_dinero && data.salones_dinero.length > 0) {
    crearChart('chart-salones-dinero', {
      type: 'bar',
      data: {
        labels: data.salones_dinero.map(item => item.nombre),
        datasets: [{
          label: 'Dinero Generado ($)',
          data: data.salones_dinero.map(item => item.dinero_generado),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } } 
      }
    });
  }

  // Salones mas usados por tipo de evento
  console.log('Chart 9b - Data:', data.salones_evento);
  if (data.salones_evento && data.salones_evento.length > 0) {
    crearChart('chart-salones-evento', {
      type: 'bar',
      data: {
        labels: data.salones_evento.map(item => `${item.tipo_evento} - ${item.salon}`),
        datasets: [{
          label: 'Frecuencia',
          data: data.salones_evento.map(item => item.frecuencia),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // ==========================================
  // TAB: MONTAJES
  // ==========================================
  
  // Tipos de montaje mas usados
  console.log('Chart 10 - Data:', data.montajes_usados);
  if (data.montajes_usados && data.montajes_usados.length > 0) {
    crearChart('chart-montajes-usados', {
      type: 'bar',
      data: {
        labels: data.montajes_usados.map(item => item.nombre),
        datasets: [{
          label: 'Frecuencia',
          data: data.montajes_usados.map(item => item.frecuencia),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } } 
      }
    });
  }

  // Tipos de montaje mas usados por tipo de evento
  console.log('Chart 10b - Data:', data.montajes_evento);
  if (data.montajes_evento && data.montajes_evento.length > 0) {
    crearChart('chart-montajes-evento', {
      type: 'bar',
      data: {
        labels: data.montajes_evento.map(item => `${item.tipo_evento} - ${item.montaje}`),
        datasets: [{
          label: 'Frecuencia',
          data: data.montajes_evento.map(item => item.frecuencia),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
  
  // ==========================================
  // TAB: PAQUETES
  // ==========================================
  
  // Combinaciones populares
  console.log('Chart 11 - Data:', data.combinaciones_populares);
  if (data.combinaciones_populares && data.combinaciones_populares.length > 0) {
    crearChart('chart-combinaciones', {
      type: 'bar',
      data: {
        labels: data.combinaciones_populares.map(item => `${item.tipo_evento} + ${item.montaje} + ${item.salon}`),
        datasets: [{
          label: 'Frecuencia',
          data: data.combinaciones_populares.map(item => item.frecuencia),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } } 
      }
    });
  }
  
  // Top servicios por tipo de evento
  console.log('Chart 12 - Data:', data.servicios_top_por_evento);
  if (data.servicios_top_por_evento && data.servicios_top_por_evento.length > 0) {
    crearChart('chart-top-servicios', {
      type: 'bar',
      data: {
        labels: data.servicios_top_por_evento.map(item => `${item.tipo_evento}: ${item.servicio}`),
        datasets: [{
          label: 'Frecuencia',
          data: data.servicios_top_por_evento.map(item => item.frecuencia),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        indexAxis: 'y',
        scales: { x: { beginAtZero: true } } 
      }
    });
  }
  
  // Top equipamiento por tipo de evento
  console.log('Chart 13 - Data:', data.equipamiento_top_por_evento);
  if (data.equipamiento_top_por_evento && data.equipamiento_top_por_evento.length > 0) {
    crearChart('chart-top-equipamiento', {
      type: 'bar',
      data: {
        labels: data.equipamiento_top_por_evento.map(item => `${item.tipo_evento}: ${item.equipamiento}`),
        datasets: [{
          label: 'Cantidad',
          data: data.equipamiento_top_por_evento.map(item => item.cantidad_total),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        indexAxis: 'y',
        scales: { x: { beginAtZero: true } } 
      }
    });
  }
  
  // Top mobiliario por tipo de evento
  console.log('Chart 14 - Data:', data.mobiliario_top_por_evento);
  if (data.mobiliario_top_por_evento && data.mobiliario_top_por_evento.length > 0) {
    crearChart('chart-top-mobiliario', {
      type: 'bar',
      data: {
        labels: data.mobiliario_top_por_evento.map(item => `${item.tipo_evento}: ${item.mobiliario}`),
        datasets: [{
          label: 'Cantidad',
          data: data.mobiliario_top_por_evento.map(item => item.cantidad_total),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        indexAxis: 'y',
        scales: { x: { beginAtZero: true } } 
      }
    });
  }
  
  // Precios promedio por evento
  console.log('Chart 15 - Data:', data.precios_promedio_evento);
  if (data.precios_promedio_evento && data.precios_promedio_evento.length > 0) {
    crearChart('chart-precios-promedio', {
      type: 'bar',
      data: {
        labels: data.precios_promedio_evento.map(item => `${item.tipo_evento} (${item.total_reservaciones})`),
        datasets: [{
          label: 'Promedio Total ($)',
          data: data.precios_promedio_evento.map(item => item.promedio_total),
          backgroundColor: backgroundColor,
          borderWidth: 1
        }]
      },
      options: { 
        responsive: true, 
        maintainAspectRatio: false, 
        scales: { y: { beginAtZero: true } } 
      }
    });
  }
  
  console.log('=== Chart.js Loading Complete ===');
});
