
/*$(document).ready(function() {
   
    var dt_table = $('.datatable').dataTable({
        language: dt_language,  // global variable defined in html
        order: [[ 1, "desc" ]],
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        columnDefs: [
            {
             name: 'id',  
             targets: [0],
             orderable: false,
             searchable: true,
             className: "center",
             visible: true,
            },
            { 
             name: 'capital_prestado',
             targets: [1],
             orderable: true,
             searchable: false,
             className: "center"
            },
            { 
             name: 'fecha_prestamo',
             targets: [2],
             orderable: true,
             searchable: false,
             className: "center"
            },
            { 
             name: 'porcentaje_aplicado__porcentaje',
             targets: [3],
             orderable: true,
             searchable: true,
             className: "center"
             
            },
            { 
             name: 'abonos_capital',
             targets: [4],
             orderable: false,
             searchable: false,
             className: "center"
            },
            //{ 
             //name: 'saldo_capital',
             //targets: [5],
             //orderable: false,
             //searchable: false,
             //className: "center"
             
            //},
            { 
             name: 'accion',
             targets: [6],
             orderable: false,
             searchable: false,
             className: "center"
             
            }
        ],
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        ajax: USERS_LIST_JSON_URL
    
    });

    
});  */

function cargarPrestamosTodos(){

    //console.log("Dentro de la funcion cargar prestamos ");
    const dt_table = $('#tablalistadoPrestamosTodos').dataTable({
        destroy: true,
        language: dt_language,  // global variable defined in html
        order: [[ 1, "desc" ]],
        lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
        columnDefs: [
            {
             name: 'id',  
             targets: [0],
             orderable: false,
             searchable: true,
             className: "center",
             visible: true,
            },
            { 
             name: 'fecha_prestamo',
             targets: [1],
             orderable: true,
             searchable: false,
             className: "center"
            },
            { 
             name: 'cliente',
             targets: [2],
             orderable: true,
             searchable: false,
             className: "center"
            },
              { 
             name: 'cliente',
             targets: [2],
             orderable: true,
             searchable: false,
             className: "center"
            },
            { 
             name: 'capital_prestado',
             targets: [3],
             orderable: true,
             searchable: true,
             className: "center"
             
            },
            { 
                name: 'tipo_prestamo',
                targets: [4],
                orderable: true,
                searchable: true,
                className: "center"
                
               }
            
            
        ],
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        paging: true,
        info: true,
        "ajax": {
            "url": PRESTAMOS_TODOS_LIST_JSON_URL,
            //"data": {"id_prestamo": id_prestamo},
        }
        //ajax: USERS_LIST_JSON_URL
    
    });





}

function cargarClientes() {
   // console.log("Dentro de la funcion cargar clientes ");
    const dt_table = $('#tablaClientes').dataTable({
        destroy: true,
        language: dt_language,  // global variable defined in html
        order: [[ 1, "desc" ]],
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        columnDefs: [
            {
             name: 'id',  
             targets: [0],
             orderable: false,
             searchable: true,
             className: "center",
             visible: false,
            },
            { 
             name: 'cedula',
             targets: [1],
             orderable: true,
             searchable: false,
             className: "center"
            },
            { 
             name: 'nombres',
             targets: [2],
             orderable: true,
             searchable: false,
             className: "center"
            },
            { 
             name: 'apellidos',
             targets: [3],
             orderable: true,
             searchable: true,
             className: "center"
             
            },
            { 
                name: 'telefono_celular',
                targets: [4],
                orderable: true,
                searchable: true,
                className: "center"
                
               }
            
            
        ],
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        paging: true,
        info: true,
        "ajax": {
            "url": CLIENTES_LIST_JSON_URL,
            //"data": {"id_prestamo": id_prestamo},
        }
        //ajax: USERS_LIST_JSON_URL
    
    });
}; 


function cargarAbonos(id_prestamo) {
    //console.log("Dentro de la funcion cargarAbonos, id_prestamo "+ id_prestamo);
    const dt_table = $('#tablaAbonos').dataTable({
        destroy: true,
        language: dt_language,  // global variable defined in html
        order: [[ 1, "desc" ]],
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        columnDefs: [
            {
             name: 'id',  
             targets: [0],
             orderable: false,
             searchable: true,
             className: "center",
             visible: true,
            },
            { 
             name: 'fecha_abono',
             targets: [1],
             orderable: true,
             searchable: false,
             className: "center"
            },
            { 
             name: 'valor_abono_capital',
             targets: [2],
             orderable: true,
             searchable: false,
             className: "center"
            },
            { 
             name: 'valor_abono_interes',
             targets: [3],
             orderable: true,
             searchable: true,
             className: "center"
             
            },
            { 
             name: 'accion',
             targets: [4],
             orderable: true,
             searchable: true,
             className: "center"
             
            }
            
        ],
        searching: false,
        processing: true,
        serverSide: true,
        stateSave: true,
        paging: false,
        info: false,
        "ajax": {
            "url": ABONOS_LIST_JSON_URL,
            "data": {"id_prestamo": id_prestamo},
        }
        //ajax: USERS_LIST_JSON_URL
    
    });
}; 

function cargarDescuentos(id_prestamo) {
    
    const dt_table = $('#tablaDescuentos').dataTable({
        destroy: true,
        language: dt_language,  // global variable defined in html
        order: [[ 1, "desc" ]],
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        columnDefs: [
            {
             name: 'id',  
             targets: [0],
             orderable: false,
             searchable: true,
             className: "center",
             visible: true,
            },
            { 
             name: 'fecha_descuento',
             targets: [1],
             orderable: true,
             searchable: false,
             className: "center"
            },
            { 
             name: 'valor_descuento',
             targets: [2],
             orderable: false,
             searchable: false,
             className: "center"
            }
            
        ],
        searching: false,
        processing: true,
        serverSide: true,
        stateSave: true,
        paging: false,
        info: false,
        "ajax": {
            "url": DESCUENTOS_LIST_JSON_URL,
            "data": {"id_prestamo": id_prestamo},
        }
        //ajax: USERS_LIST_JSON_URL
    
    });
}; 

function cargarPrestamos(id_cliente) {
    //console.log("Dentro de la funcion cargarPrestamos");
    const dt_table = $('#tablaPrestamos').dataTable({
        destroy: true,
        language: dt_language,  // global variable defined in html
        order: [[ 1, "desc" ]],
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        columnDefs: [
            {
             name: 'id',  
             targets: [0],
             orderable: false,
             searchable: true,
             className: "center",
             visible: true,
            },
            { 
             name: 'capital_prestado',
             targets: [1],
             orderable: true,
             searchable: false,
             className: "center"
            },
            { 
             name: 'fecha_prestamo',
             targets: [2],
             orderable: true,
             searchable: false,
             className: "center"
            },
            { 
             name: 'porcentaje_aplicado__porcentaje',
             targets: [3],
             orderable: true,
             searchable: true,
             className: "center"
             
            },
            { 
             name: 'abonos_capital',
             targets: [4],
             orderable: false,
             searchable: false,
             className: "center"
            },
            //{ 
             //name: 'saldo_capital',
             //targets: [5],
             //orderable: false,
             //searchable: false,
             //className: "center"
             
            //},
            { 
             name: 'accion',
             targets: [6],
             orderable: false,
             searchable: false,
             className: "center"
             
            }
        ],
        searching: false,
        processing: true,
        serverSide: true,
        stateSave: true,
        paging: false,
        info: false,
        "ajax": {
            "url": USERS_LIST_JSON_URL,
            "data": {"id_cliente": id_cliente},
        }
        //ajax: USERS_LIST_JSON_URL
    
    });
}; 


function cargarTodosLosPrestamos() {
    //console.log("Dentro de la funcion cargarPrestamos");
    const dt_table = $('#tablaPrestamos_reporte').dataTable({
        destroy: true,
        language: dt_language,  // global variable defined in html
        order: [[ 1, "desc" ]],
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        columnDefs: [
            {
             name: 'id',  
             targets: [0],
             orderable: false,
             searchable: false,
             className: "center",
             visible: true,
            },
           
            { 
             name: 'capital_prestado',
             targets: [1],
             orderable: true,
             searchable: true,
             className: "center"
            },
            { 
             name: 'fecha_prestamo',
             targets: [2],
             orderable: false,
             searchable: false,
             className: "center"
             
            },
            { 
             name: 'porcentaje_aplicado__porcentaje',
             targets: [3],
             orderable: false,
             searchable: false,
             className: "center"
             
            },
            {
                name: 'cliente',  
                targets: [4],
                orderable: true,
                searchable: true,
                className: "center",
                visible: true,
            },
            { 
             name: 'abonos_capital',
             targets: [5],
             orderable: false,
             searchable: false,
             className: "center"
            },
            { 
                name: 'descuentos',
                targets: [6],
                orderable: false,
                searchable: false,
                className: "center"
                
            },
            { 
             name: 'saldo_capital',
             targets: [7],
             orderable: false,
             searchable: false,
             className: "center"
             
            }
            /*{ 
             name: 'accion',
             targets: [6],
             orderable: false,
             searchable: false,
             className: "center"
             
            }*/
        ],
        searching: true,
        processing: true,
        serverSide: true,
        stateSave: true,
        paging: true,
        info: true,
        "ajax": {
            "url": TODOS_PRESTAMOS_JSON_URL,
            
        }
        //ajax: USERS_LIST_JSON_URL
    
    });
}; 




