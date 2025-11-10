create table ingredient
(
    id         int auto_increment
        primary key,
    food_name  varchar(200)                       not null,
    ingredient text                               null,
    path       varchar(500)                       null,
    created_at datetime default CURRENT_TIMESTAMP null,
    updated_at datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
);

create index idx_food_name
    on ingredient (food_name);

create table permission
(
    id          int auto_increment
        primary key,
    name        varchar(80)  not null,
    description varchar(255) null,
    constraint name
        unique (name)
);

create index idx_permission_name
    on permission (name);

create table role
(
    id   int auto_increment
        primary key,
    name varchar(80) not null,
    constraint name
        unique (name)
);

create index idx_role_name
    on role (name);

create table role_permissions
(
    role_id       int not null,
    permission_id int not null,
    primary key (role_id, permission_id),
    constraint role_permissions_ibfk_1
        foreign key (role_id) references role (id)
            on delete cascade,
    constraint role_permissions_ibfk_2
        foreign key (permission_id) references permission (id)
            on delete cascade
);

create index permission_id
    on role_permissions (permission_id);

create table users
(
    id              int auto_increment
        primary key,
    username        varchar(80)                           not null,
    password        varchar(255)                          not null,
    email           varchar(120)                          null,
    first_name      varchar(50)                           null,
    last_name       varchar(50)                           null,
    display_name    varchar(100)                          null,
    sso_provider    varchar(50)                           null comment 'SSO提供者类型',
    sso_subject     varchar(255)                          null comment 'SSO提供者的用户ID',
    last_login      datetime                              null comment '最后登录时间',
    role_id         int                                   null,
    status          varchar(20) default 'pending'         null comment '用户状态: pending, approved, rejected',
    register_time   datetime    default CURRENT_TIMESTAMP null,
    approve_time    datetime                              null,
    approve_user_id int                                   null,
    constraint email
        unique (email),
    constraint username
        unique (username),
    constraint users_ibfk_1
        foreign key (role_id) references role (id)
            on delete set null,
    constraint users_ibfk_2
        foreign key (approve_user_id) references users (id)
            on delete set null
);

create table stop_words
(
    id         int auto_increment
        primary key,
    word       varchar(100)                       not null,
    created_at datetime default CURRENT_TIMESTAMP null,
    user_id    int                                not null,
    constraint unique_word_per_user
        unique (word, user_id),
    constraint stop_words_ibfk_1
        foreign key (user_id) references users (id)
            on delete cascade
);

create index idx_user_id
    on stop_words (user_id);

create index idx_word
    on stop_words (word);

create table translation
(
    id         int auto_increment
        primary key,
    english    varchar(500)                       not null,
    chinese    varchar(500)                       not null,
    user_id    int                                not null,
    created_at datetime default CURRENT_TIMESTAMP null,
    updated_at datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    constraint translation_ibfk_1
        foreign key (user_id) references users (id)
            on delete cascade
);

create index idx_english
    on translation (english(100));

create index idx_user_id
    on translation (user_id);

create table upload_records
(
    id              int auto_increment
        primary key,
    user_id         int                                   not null,
    filename        varchar(255)                          not null,
    stored_filename varchar(255)                          not null,
    file_path       varchar(255)                          not null,
    file_size       int                                   not null,
    upload_time     datetime    default CURRENT_TIMESTAMP null,
    status          varchar(20) default 'pending'         null,
    error_message   varchar(255)                          null,
    constraint upload_records_ibfk_1
        foreign key (user_id) references users (id)
            on delete cascade
);

create index idx_status
    on upload_records (status);

create index idx_upload_time
    on upload_records (upload_time);

create index idx_user_id
    on upload_records (user_id);

create index approve_user_id
    on users (approve_user_id);

create index idx_email
    on users (email);

create index idx_last_login
    on users (last_login);

create index idx_sso_provider
    on users (sso_provider);

create index idx_sso_subject
    on users (sso_subject);

create index idx_status
    on users (status);

create index idx_username
    on users (username);

create index role_id
    on users (role_id);

