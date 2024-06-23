# AsyncPG + Streamlit

Where SQLAlchemy async API meets multithreading.

The problem:

> got Future <Future pending cb=[Protocol._on_waiter_completed()]> attached to a different loop.

The solutions:

1. Bad

```py
from sqlalchemy.pool import NullPool


create_async_engine(
    url=database_uri,
    poolclass=NullPool,
)
```

2. Remove `metaclass=SingletonHash` from `BaseOrm` and create engine along with every database transaction, then dispose it. Also Bad.

3. At each streamlit page, ensure that the same asyncio loop is used during the user session. Nice!

```sh
if "loop" not in st.session_state:
    st.session_state["loop"] = asyncio.new_event_loop()
loop = st.session_state["loop"]
loop.run_until_complete(main())
```
