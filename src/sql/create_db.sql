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


drop table if exists hist;
create table hist (
    hist_id integer primary key,
    script  text,
    control text,
    command text,
    start   integer,
    end_    integer
);
create index hist_script on hist (script);
create index hist_control on hist (control);


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
