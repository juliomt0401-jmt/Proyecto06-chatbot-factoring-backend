from app.bd import BD
from app.logica import buscar_descripcion_tabla, consultar_ruc_api


class Proveedor:

    def __init__(self,  idProveedor:int | None = None, 
                        RUC:str | None = None, 
                        RazonSocial:str | None = None, 
                        NombreComercial:str | None = None, 
                        Telefono:str | None = None, 
                        TipoContribuyente:str | None = None,
                        Estado:str | None = None):
        self.idProveedor = idProveedor
        self.RUC = RUC
        self.RazonSocial = RazonSocial
        self.NombreComercial = NombreComercial
        self.Telefono = Telefono
        self.TipoContribuyente = TipoContribuyente
        self.DesTipoContribuyente = ""
        self.Estado = Estado
        if self.TipoContribuyente not in (None, ""):
            self.DesTipoContribuyente = buscar_descripcion_tabla("TCOS", self.TipoContribuyente)


    @staticmethod
    def consultar_proveedor(RUC):
        sql = """
            SELECT
                p.idProveedor, p.RUC, e.RazonSocial, e.NombreComercial, e.Telefono, 
                e.TipoContribuyente, t.Descripcion AS DesTipoContribuyente, p.Estado
            FROM Proveedores p INNER JOIN Empresas e
            ON e.RUC = p.RUC INNER JOIN sys_tablas t 
            ON t.idTabla = 'TCOS' AND t.idElemento = e.TipoContribuyente
            WHERE p.RUC = %s
        """
        db = BD()
        recordset = db.ejecutar_SQL(sql, (RUC,))
        if recordset:
            return recordset[0]

        razon_social = consultar_ruc_api(RUC)

        return {
            "idProveedor": 0,
            "RUC": RUC,
            "RazonSocial": razon_social,
            "NombreComercial": "",
            "Telefono": "",
            "TipoContribuyente": "",
            "DesTipoContribuyente": "",
            "Estado": ""
        }

