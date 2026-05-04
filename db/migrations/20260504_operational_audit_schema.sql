-- Core operational schema for DJI Agras audit platform
create table if not exists clientes (
  id uuid primary key,
  nome text not null,
  criado_em timestamptz default now()
);
create table if not exists fazendas (id uuid primary key, cliente_id uuid references clientes(id), nome text not null, criado_em timestamptz default now());
create table if not exists talhoes (id uuid primary key, fazenda_id uuid references fazendas(id), nome text not null, area_ha numeric, criado_em timestamptz default now());
create table if not exists operadores (id uuid primary key, nome text not null, criado_em timestamptz default now());
create table if not exists drones (id uuid primary key, modelo text not null, serial text, criado_em timestamptz default now());
create table if not exists baterias (id uuid primary key, drone_id uuid references drones(id), serial text, ciclos integer default 0, criado_em timestamptz default now());
create table if not exists produtos (id uuid primary key, nome text not null, criado_em timestamptz default now());
create table if not exists receituarios (id uuid primary key, cliente_id uuid references clientes(id), produto_id uuid references produtos(id), dose_l_ha numeric, criado_em timestamptz default now());
create table if not exists missoes (id uuid primary key, cliente_id uuid references clientes(id), fazenda_id uuid references fazendas(id), talhao_id uuid references talhoes(id), operador_id uuid references operadores(id), drone_id uuid references drones(id), inicio timestamptz, fim timestamptz, criado_em timestamptz default now());
create table if not exists voos (id uuid primary key, missao_id uuid references missoes(id), bateria_id uuid references baterias(id), inicio timestamptz, fim timestamptz, area_aplicada_ha numeric, volume_aplicado_l numeric, criado_em timestamptz default now());
create table if not exists eventos_voo (
  id uuid primary key,
  voo_id uuid not null references voos(id),
  tipo_evento text not null check (tipo_evento in ('pulverizando','manobrando','deslocando','parado','retorno_base','troca_bateria','reabastecimento')),
  inicio timestamptz,
  fim timestamptz,
  duracao_segundos integer,
  latitude double precision,
  longitude double precision,
  velocidade double precision,
  altitude double precision,
  bateria_percentual double precision,
  vazao double precision,
  volume_aplicado double precision,
  criado_em timestamptz default now()
);
create table if not exists aplicacoes (id uuid primary key, voo_id uuid references voos(id), produto_id uuid references produtos(id), dose_l_ha numeric, volume_total_l numeric, criado_em timestamptz default now());
create table if not exists abastecimentos (id uuid primary key, voo_id uuid references voos(id), volume_l numeric, criado_em timestamptz default now());
create table if not exists manutencoes (id uuid primary key, drone_id uuid references drones(id), descricao text, criado_em timestamptz default now());
create table if not exists checklists (id uuid primary key, voo_id uuid references voos(id), status text, criado_em timestamptz default now());
create table if not exists relatorios (id uuid primary key, missao_id uuid references missoes(id), resumo jsonb, criado_em timestamptz default now());
