# Auditoría de vistas y serializers

Hallazgos (sin modificar código), centrados en flujo, lógica y serializers:

- Falta `is_valid()` antes de `save()`: en `procesar_cadena()` se llama `serializer.save()` sin validar, lo que dispara `AssertionError` y no entra en los `except` actuales. Ver center_administration/views.py.

(ya lo hice revisar linea 85 de center_administration/views.py.
)


- Registro en dos pasos sin transacción: si el `User` se crea y el perfil falla, quedan datos inconsistentes y no se devuelven errores del serializer de perfil. Ver center_administration/views.py.

(Explicacion del contexto, el perfil no se puede crear sino esta logueado y tiene permiso) El user nunca puede fallar porque sino no tendria acceso a la session de crear su perfil)

- En `ReadFormView`, el serializer de perfil puede fallar porque `CenterAdministrator` exige `yoga_center` y no se aporta; solo se pasa `user`. Ver center_administration/views.py y center_administration/models.py.

(Se elimino la vista del lectura de perfil ya que se hara todo dentro de un proceso de transacion en configuracion inicial)


- `MasterSerializer` no define `Meta` (`model`/`fields`), por lo que DRF no puede validar correctamente el payload. Ver centeryoga/serializer.py.

(No lleva meta porque es un wrapper de serializer o serializer intermedio para solo decodificar el json en objecto de otro modelos y que se serializer por sus propios serializer )


- Desfase de nombres en `MasterSerializer`: se declara `center_administrator` pero se hace `pop('profile_admin_center')`, lo que provoca `KeyError`. Ver centeryoga/serializer.py.

(Solucionado revisar linea 26 yogacenter/serializer)

- `MasterSerializer` usa `Rule.create`, `RulesPackages.create`, `RulesPayment.create`, pero esos métodos no existen en los modelos. Ver centeryoga/serializer.py, rules_center/models.py, rules_packages/models.py, rules_payments/models.py.

(Solucionado ver linea 34 y demas en yogacenter/serializer)


- Relaciones no resueltas en la transacción: `RulesPackages` y `RulesPayment` requieren `rules_center` (FK), pero no se vinculan al `Rule` creado; si el payload no lo trae, fallará. Ver centeryoga/serializer.py, rules_packages/models.py, rules_payments/models.py.
(solucionado revisar serializer )

- `CenterAdministrator.activate_profile()` escribe `is_active_center`, campo inexistente; no se guarda `is_active_profile`. Ver center_administration/models.py.
(solucionado revisar center_administrator)

- `CenterSerializer.create()` devuelve instancia sin guardar, por lo que `save()` no persiste en DB si se usa directo. Ver centeryoga/serializer.py.

(no persiste porque el modelo depende de una transacion de otro modelos explicacion dicha en linea 13 de auditora.md)

- Validación de foto no corre: `validate_photo_profile` no coincide con el campo `photo`. Ver centeryoga/serializer.py y centeryoga/models.py.
- `RuleSerializer.create()` usa `Rule.create`, método inexistente. Ver rules_center/serializer.py.

solucionado 

- `RulesPackagesSerializer.create()` y `RulesPaymentSerializer.create()` no guardan (`save()`), retornan instancias no persistidas. Ver rules_packages/serializer.py y rules_payments/serializer.py.
(leer linea 13 de auditoria.md)


- `RulesPaymentSerializer` usa campos que no existen en el modelo (`promotion_percentage`, `access_duration`), mientras el modelo tiene `discoint_percentage`, `comission_percentage`. Ver rules_payments/serializer.py y rules_payments/models.py.
(solucionado)

- `CenterAdministratorSerializer.delete()` no es parte del contrato estándar de DRF para serializers y además referencia `instance.center_admin` (atributo inexistente). Ver center_administration/serializer.py y center_administration/models.py.
solucionado

- Import circular probable: `centeryoga/serializer.py` importa `CenterSerializer` desde el mismo módulo, innecesario y puede romper carga. Ver centeryoga/serializer.py.
(solucionado)

