from django.db import models

class Rubro(models.Model):
	nombre = models.CharField(max_length=35)
	descripcion = models.TextField(max_length=100, help_text='Descripcion de que trata el rubro (carpinteria, ferreteria, veterinaria)')
	modificado = models.DateTimeField(auto_now=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return '{}'.format(self.nombre)
	class Meta:
		ordering = ["nombre"]

class Grupo(models.Model):
	nombre = models.CharField(max_length=35)
	descripcion = models.TextField(max_length=100, help_text='Descripcion de que trata el grupo del articulo (alimenos, mascotas, farmaceutica)')
	modificado = models.DateTimeField(auto_now=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return '{}'.format(self.nombre)
	class Meta:
		ordering = ["nombre"]

class SubGrupo(models.Model):
	Grupo = models.ForeignKey(Grupo, null=False,blank=False, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=35)
	descripcion = models.TextField(max_length=100, help_text='Detallado características del producto (vegetarianos, perros, farmacias, supermercado, )')
	modificado = models.DateTimeField(auto_now=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return '{}'.format(self.nombre)
	class Meta:
		ordering = ["Grupo","nombre"]

class Articulo(models.Model):
	SubGrupo = models.ManyToManyField(SubGrupo,blank=True)
	Rubro = models.ManyToManyField(Rubro,blank=True)
	Relacionado = models.ManyToManyField('self',blank=True, help_text='El artículo relacionado es aquel producto que acompaña al principal (De un celular distintas carcasas)')
	Similar = models.ManyToManyField('self',blank=True, help_text='El artículo similar viene siendo el artículo de la competencia de fabrica distinta')
	codigo_ean = models.CharField(max_length=13,help_text='EAN o EAN13, Número de Artículo Internacional (originalmente European Article Number)')
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField(help_text='Descripción del artículo')
	activado = models.BooleanField(default=False,help_text='Valida datos reales')
	caracteristicas = models.TextField(help_text='Características técnicas del producto')
	modificado = models.DateTimeField(auto_now=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return '{} {}'.format(self.codigo_ean, self.nombre)
	class Meta:
		verbose_name = 'Artículo'
		verbose_name_plural = 'Artículos'
		ordering = ["codigo_ean","nombre"]
