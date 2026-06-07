document.addEventListener('DOMContentLoaded', function() {
  // === SERVICIOS ===
  const tiposServicio = document.querySelectorAll('.administrador-tbody tr').length > 0 ? window.tiposServicio || [] : [];
  
  if (typeof configurarInlineEdit === 'function' && document.querySelector('.administrador-tbody')) {
    configurarInlineEdit({
      nombreSingular: 'servicio',
      urlActualizar: '/administracion/servicios/0/actualizar/',
      campoObligatorio: 'nombre',
      campoNombre: 'nombre',
      campos: [
        { nombre: 'nombre', clase: 'celda-nombre', tipo: 'texto' },
        { nombre: 'tipo_servicio', clase: 'celda-tipo', tipo: 'select-db', opcionesVar: 'tiposServicio', dataAttr: 'tipoId' },
        { nombre: 'descripcion', clase: 'celda-descripcion', tipo: 'texto' },
        { nombre: 'costo', clase: 'celda-costo', tipo: 'numero' },
        { nombre: 'disposicion', clase: 'celda-disposicion', tipo: 'booleano' }
      ]
    });
  }

  // === EQUIPAMIENTO ===
  const tiposEquipamiento = document.querySelectorAll('.administrador-tbody tr').length > 0 ? window.tiposEquipamiento || [] : [];
  
  if (typeof configurarInlineEdit === 'function' && document.getElementById('filtro-tipo')) {
    configurarInlineEdit({
      nombreSingular: 'equipamiento',
      urlActualizar: '/administracion/equipamiento/0/actualizar/',
      campoObligatorio: 'nombre',
      campoNombre: 'nombre',
      campos: [
        { nombre: 'nombre', clase: 'celda-nombre', tipo: 'texto' },
        { nombre: 'tipo_equipa', clase: 'celda-tipo', tipo: 'select-db', opcionesVar: 'tiposEquipamiento', dataAttr: 'tipoId' },
        { nombre: 'descripcion', clase: 'celda-descripcion', tipo: 'texto' },
        { nombre: 'costo', clase: 'celda-costo', tipo: 'numero' },
        { nombre: 'stock', clase: 'celda-stock', tipo: 'numero' }
      ]
    });
  }

  // === MOBILIARIO ===
  const tiposMobil = document.querySelectorAll('.administrador-tbody tr').length > 0 ? window.tiposMobil || [] : [];
  
  if (typeof configurarInlineEdit === 'function' && document.getElementById('filtro-tipo')) {
    configurarInlineEdit({
      nombreSingular: 'mobiliario',
      urlActualizar: '/administracion/mobiliario/0/actualizar/',
      campoObligatorio: 'nombre',
      campoNombre: 'nombre',
      campos: [
        { nombre: 'nombre', clase: 'celda-nombre', tipo: 'texto' },
        { nombre: 'tipo_movil', clase: 'celda-tipo', tipo: 'select-db', opcionesVar: 'tiposMobil', dataAttr: 'tipoId' },
        { nombre: 'descripcion', clase: 'celda-descripcion', tipo: 'texto' },
        { nombre: 'costo', clase: 'celda-costo', tipo: 'numero' },
        { nombre: 'stock', clase: 'celda-stock', tipo: 'numero' }
      ]
    });
  }

  // === SALONES ===
  if (typeof configurarInlineEdit === 'function' && document.querySelector('.salones-tabla')) {
    configurarInlineEdit({
      nombreSingular: 'salon',
      urlActualizar: '/administracion/salones/0/actualizar/',
      campoObligatorio: 'nombre',
      campoNombre: 'nombre',
      campos: [
        { nombre: 'nombre', clase: 'celda-nombre', tipo: 'texto' },
        { nombre: 'costo', clase: 'celda-costo', tipo: 'numero' },
        { nombre: 'ubicacion', clase: 'celda-ubicacion', tipo: 'texto' },
        { nombre: 'estado_salon', clase: 'celda-estado', tipo: 'select' }
      ]
    });
  }
});