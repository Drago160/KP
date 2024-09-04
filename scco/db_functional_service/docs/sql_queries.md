Map messages to files of generated offers:
```postgresql
select message, file_path
from offer join query using (query_id)
;
```
