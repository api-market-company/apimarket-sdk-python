from typing import List, Optional
from pydantic import BaseModel, Field

class Regimen(BaseModel):
    cregimen: str
    dregimen: str
    faltaReg: str = Field(alias='faltaReg')
    fbajaReg: Optional[str] = Field(alias='fbajaReg')
    fefecAReg: str = Field(alias='fefecAReg')
    fefecBReg: Optional[str] = Field(alias='fefecBReg')

class CodigoPostal(BaseModel):
    clave: str
    esMatriz: bool = Field(alias='esMatriz')

class Obligacion(BaseModel):
    cvePago: str = Field(alias='cvePago')
    cobligacion: str = Field(alias='cobligacion')
    dobligacion: str = Field(alias='dobligacion')
    faltaOblig: str = Field(alias='faltaOblig')
    fbajaOblig: str = Field(alias='fbajaOblig')
    fefecAOblig: str = Field(alias='fefecAOblig')
    fefecBOblig: str = Field(alias='fefecBOblig')
    finiLegal: str = Field(alias='finiLegal')
    ffinLegal: Optional[str] = Field(alias='ffinLegal')
    tcontribucion: str = Field(alias='tcontribucion')
    dobligLc: str = Field(alias='dobligLc')

class FiscalDataResponse(BaseModel):
    rfc: str
    nombreCompleto: str = Field(alias='nombreCompleto')
    tipoPersona: str = Field(alias='tipoPersona')
    correoElectronico: str = Field(alias='correoElectronico')
    puedeFacturar: bool = Field(alias='puedeFacturar')
    regimenes: List[Regimen]
    codigosPostales: List[CodigoPostal] = Field(alias='codigosPostales')
    actividades: Optional[List[str]] = None
    obligaciones: List[Obligacion]
