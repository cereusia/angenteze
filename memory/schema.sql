create table if not exists kv_store (
  key text primary key,
  value text not null,
  updated_at text not null
);

create table if not exists interactions (
  id integer primary key autoincrement,
  request_id text not null unique,
  source text not null,
  prompt text not null,
  response_status text not null,
  response_message text not null,
  created_at text not null
);

create index if not exists idx_interactions_created_at
  on interactions(created_at);
