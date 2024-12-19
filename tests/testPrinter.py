from backend.modules.ticketPrinter_module import TicketPrinter

# Crear una instancia de TicketPrinter
printer = TicketPrinter()
# Agregar productos de ejemplo
                          
printer.agregar_producto("Pack Jabón Sensación Humectante Oliva y Aloe Palmolive 330g", 2, 3.50)

# Imprimir el ticket en el terminal
printer.imprimir_ticket()
