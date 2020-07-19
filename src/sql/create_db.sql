drop table if exists docs;
create table docs (
    doc_id    text primary key,
    path      text,
    loaded    text,
    edited    text,
    extracted text,
    method    text,
    raw       text,
    edits     text
);


drop table if exists pipes;
create table pipes (
    pipe_id text primary key,
    pipe    blob,
    order_  integer,
    parent  text
);
create index pipes_parent on pipes (parent);
create index pipes_order on pipes (pipe_id, order_);


drop table if exists traits;
create table traits (
    trait_id integer primary key,
    doc_id   text,
    trait    text,
    start    integer,
    end_     integer
);
create index traits_doc_id on traits (doc_id);
create index traits_trait on traits (trait);
create index traits_pos on traits (start, end_);


drop table if exists props;
create table props (
    prop_id   integer primary key,
    trait_id  integer,
    name      text,
    val       blob
);
create index props_trait_id on props (trait_id);
create index props_name on props (name);
create index props_val_int   on props (cast(val as integer));
create index props_val_text  on props (cast(val as text));
create index props_val_real  on props (cast(val as real));
