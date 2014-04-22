create table antrag (
      id integer primary key autoincrement,
      msg_id string unique,
      subject string,
      ub string, -- unique
      starter string,
      public boolean
);

create table votes (
    id integer primary key autoincrement,
    antrag integer references antrag,
    vorstand integer references vorstand,
    text string,
    sig string,
    state integer,
    verified boolean,
    unique (vorstand, antrag)
);

create table vorstand (
      id integer primary key autoincrement,
      name string,
      short string,
      email string,
      pass string,
      pubkey string
);

create table msgs (
    id integer primary key autoincrement,
    msg_id string unique,
    thread_id string
);

insert into vorstand (name, short, email, pass, pubkey) VALUES
    ( 'a', 'b', 'a@b.c', '0363f1a98b0c507a237977267358886724194e58198ae5efc58c659238ee8fc3', 'key'),
