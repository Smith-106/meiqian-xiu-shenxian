CREATE TABLE agency_activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    event_type TEXT NOT NULL,   -- 'activity' | 'progress'
    role TEXT,                  -- activity: lead_writer/producer/editor_auditor
    action TEXT,                -- activity: start/done
    detail TEXT,                -- activity: 概念/首章/深度资产/审查/装配
    phase TEXT,                 -- progress: concept/assets/writing/review/assembly
    status TEXT,                -- progress: running/completed/failed
    message TEXT,               -- progress: 描述文案
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE agency_agent_tasks (
                id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                story_id TEXT NOT NULL,
                role TEXT NOT NULL,
                parent_task_id TEXT,
                task TEXT NOT NULL,
                status TEXT NOT NULL,
                phase TEXT,
                turn_count INTEGER NOT NULL DEFAULT 0,
                tool_calls INTEGER NOT NULL DEFAULT 0,
                last_tool TEXT,
                heartbeat_at TEXT,
                started_at TEXT,
                finished_at TEXT,
                error TEXT,
                result_summary TEXT,
                meta_json TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE agency_board_items (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    story_id TEXT NOT NULL,
    zone TEXT NOT NULL,
    item_type TEXT NOT NULL,
    key TEXT NOT NULL,
    content TEXT NOT NULL DEFAULT '',
    summary TEXT NOT NULL DEFAULT '',
    version INTEGER NOT NULL DEFAULT 1,
    producer TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE agency_chat_messages (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                status TEXT NOT NULL,
                run_key TEXT,
                task_id TEXT,
                task_ids_json TEXT,
                actions_json TEXT,
                meta_json TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES agency_chat_sessions(id) ON DELETE CASCADE
            );

CREATE TABLE agency_chat_sessions (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                title TEXT NOT NULL,
                target_role TEXT NOT NULL DEFAULT 'director',
                summary TEXT,
                summary_upto_message_id TEXT,
                archived INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE agency_checkpoints (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    story_id TEXT NOT NULL,
    milestone TEXT NOT NULL,
    chapter_number INTEGER,
    metrics_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);

CREATE TABLE agency_director_actions (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                session_id TEXT,
                message_id TEXT,
                run_id TEXT,
                action_type TEXT NOT NULL,
                target_role TEXT,
                target_id TEXT,
                params_json TEXT NOT NULL DEFAULT '{}',
                status TEXT NOT NULL,
                reason TEXT,
                result_summary TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE agency_messages (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    from_role TEXT NOT NULL,
    to_role TEXT NOT NULL,
    msg_type TEXT NOT NULL,
    payload TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);

CREATE TABLE agency_runs (
    id TEXT PRIMARY KEY,
    story_id TEXT,
    premise TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    phase TEXT NOT NULL DEFAULT 'concept',
    result_json TEXT,
    error_message TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
, lane TEXT NOT NULL DEFAULT 'write');

CREATE TABLE agency_sessions (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    story_id TEXT,
    phase TEXT NOT NULL,
    snapshot_json TEXT NOT NULL DEFAULT '{}',
    summary TEXT,
    kind TEXT NOT NULL DEFAULT 'auto',
    created_at TEXT NOT NULL
);

CREATE TABLE ai_operations (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    scene_id TEXT,
                    chapter_id TEXT,
                    operation_type TEXT NOT NULL,
                    operation_name TEXT NOT NULL,
                    input_summary TEXT,
                    output_summary TEXT,
                    previous_content TEXT,
                    new_content TEXT,
                    metadata TEXT,
                    status TEXT NOT NULL DEFAULT 'success',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
                );

CREATE TABLE ai_usage_logs (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    story_id TEXT,
                    chapter_id TEXT,
                    agent_type TEXT NOT NULL,
                    instruction TEXT,
                    prompt_tokens INTEGER,
                    completion_tokens INTEGER,
                    model_used TEXT,
                    cost REAL,
                    duration_ms INTEGER,
                    tier_at_time TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

CREATE TABLE app_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

CREATE TABLE asset_asset_edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_asset_id TEXT NOT NULL,
    target_asset_id TEXT NOT NULL,
    edge_type TEXT NOT NULL,            -- 'tool_next' | 'tool_cooccur' | 'depends_on' | 'complements'
    weight REAL NOT NULL DEFAULT 1.0,
    cooccurrence_count INTEGER NOT NULL DEFAULT 1,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    FOREIGN KEY (source_asset_id) REFERENCES asset_nodes(id) ON DELETE CASCADE,
    FOREIGN KEY (target_asset_id) REFERENCES asset_nodes(id) ON DELETE CASCADE,
    UNIQUE(source_asset_id, target_asset_id, edge_type)
);

CREATE TABLE asset_nodes (
    id TEXT PRIMARY KEY,
    asset_type TEXT NOT NULL,           -- 'skill' | 'methodology' | 'style_dna' | 'genre_profile' | 'mcp_tool' | 'agent' | 'system_command'
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    embedding BLOB,                     -- 语义嵌入向量
    capability_id TEXT,               -- 关联到 CapabilityRegistry 的 ID
    metadata TEXT,                    -- JSON: { parameters, constraints, tags, ... }
    frequency INTEGER NOT NULL DEFAULT 1,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

CREATE TABLE beat_technique_log (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                scene_id TEXT,
                chapter_number INTEGER NOT NULL,
                beat_no INTEGER NOT NULL,
                technique_id TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

CREATE TABLE blueprints (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                chapter_number INTEGER NOT NULL,
                title TEXT,
                role TEXT,
                purpose TEXT,
                key_events TEXT,
                characters TEXT,
                suspense_hook TEXT,
                user_guidance TEXT,
                notes TEXT,
                notes_updated_at TEXT,
                knowledge_query_hint TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
                UNIQUE(story_id, chapter_number)
            );

CREATE TABLE cascade_impacts (
    id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    batch_id TEXT NOT NULL,
    source_scene_id TEXT NOT NULL,
    source_chapter_number INTEGER,
    target_scene_id TEXT NOT NULL,
    target_chapter_number INTEGER,
    impact_score REAL NOT NULL DEFAULT 0,
    impact_kind TEXT NOT NULL DEFAULT 'mention',
    severity TEXT NOT NULL DEFAULT 'info',
    entity_ids TEXT NOT NULL DEFAULT '[]',
    detail TEXT,
    evidence TEXT,
    decision TEXT NOT NULL DEFAULT 'open',
    stale_flag INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(batch_id, target_scene_id),
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE change_tracks (
            id TEXT PRIMARY KEY,
            scene_id TEXT,
            chapter_id TEXT,
            version_id TEXT,
            author_id TEXT NOT NULL,
            author_name TEXT,
            change_type TEXT NOT NULL,
            from_pos INTEGER NOT NULL,
            to_pos INTEGER NOT NULL,
            content TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL,
            resolved_at TEXT,
            FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE CASCADE,
            FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE,
            FOREIGN KEY (version_id) REFERENCES scene_versions(id) ON DELETE CASCADE
        );

CREATE TABLE chapter_reading_power (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                scene_id TEXT,
                chapter_number INTEGER NOT NULL,
                hook_type TEXT,
                hook_strength TEXT DEFAULT 'medium',
                coolpoint_patterns_json TEXT,
                micropayoffs_json TEXT,
                hard_violations_json TEXT,
                soft_suggestions_json TEXT,
                is_transition INTEGER NOT NULL DEFAULT 0,
                override_count INTEGER NOT NULL DEFAULT 0,
                debt_balance REAL NOT NULL DEFAULT 0.0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
                FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE SET NULL
            );

CREATE TABLE chapters (
            id TEXT PRIMARY KEY,
            story_id TEXT NOT NULL,
            chapter_number INTEGER NOT NULL,
            title TEXT,
            outline TEXT,
            word_count INTEGER,
            model_used TEXT,
            cost REAL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL, writing_phase TEXT DEFAULT 'planning',
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
            UNIQUE(story_id, chapter_number)
        );

CREATE TABLE character_aliases (
    id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    character_id TEXT NOT NULL,
    alias TEXT NOT NULL,
    source TEXT NOT NULL DEFAULT 'ingest',
    created_at TEXT NOT NULL,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
    FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
);

CREATE TABLE character_emotion_states (
  id TEXT PRIMARY KEY,
  story_id TEXT NOT NULL,
  character_id TEXT NOT NULL,
  scene_id TEXT,
  chapter_number INTEGER,
  beat_index INTEGER,
  vector_json TEXT NOT NULL,
  intensity REAL NOT NULL DEFAULT 0.5,
  active_goal TEXT,
  defense TEXT,
  cause_event TEXT,
  source TEXT NOT NULL DEFAULT 'ingest',
  created_at TEXT NOT NULL,
  FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE character_knowledge_log (
    id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    character_id TEXT NOT NULL,
    fact TEXT NOT NULL,
    change_type TEXT NOT NULL DEFAULT 'learned',
    source_scene_id TEXT,
    chapter_number INTEGER,
    evidence TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE character_names (
    character_id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    formal TEXT NOT NULL,
    surname TEXT,
    generation TEXT,
    given TEXT,
    courtesy TEXT,
    art TEXT,
    childhood TEXT,
    nickname TEXT,
    aliases_json TEXT NOT NULL DEFAULT '[]',
    titles_json TEXT NOT NULL DEFAULT '[]',
    taboo_json TEXT NOT NULL DEFAULT '[]',
    address_rules_json TEXT NOT NULL DEFAULT '[]',
    name_story TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE character_relationships (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                source_character_id TEXT NOT NULL,
                target_character_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                description TEXT,
                dynamic TEXT,
                created_at TEXT NOT NULL, emotional_bond TEXT, emotional_intensity REAL DEFAULT 0.5, reverse_emotional_bond TEXT, reverse_emotional_intensity REAL DEFAULT 0.5, relation_kind TEXT, relation_flags INTEGER,
                FOREIGN KEY (source_character_id) REFERENCES characters(id) ON DELETE CASCADE,
                FOREIGN KEY (target_character_id) REFERENCES characters(id) ON DELETE CASCADE
            );

CREATE TABLE character_states (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    character_id TEXT NOT NULL,
                    current_location TEXT,
                    current_emotion TEXT,
                    active_goal TEXT,
                    secrets_known TEXT,
                    secrets_unknown TEXT,
                    arc_progress REAL,
                    last_updated TEXT, state_transitions_json TEXT DEFAULT '[]', arc_type TEXT DEFAULT 'positive', location TEXT, power_level TEXT, physical_state TEXT, mental_state TEXT, key_items TEXT, recent_events TEXT, updated_at_chapter INTEGER, cs_json TEXT,
                    FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
                );

CREATE TABLE characters (
            id TEXT PRIMARY KEY,
            story_id TEXT NOT NULL,
            name TEXT NOT NULL,
            background TEXT,
            personality TEXT,
            goals TEXT,
            dynamic_traits TEXT, -- JSON array
            source TEXT DEFAULT 'user_created',
            is_auto_generated INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL, appearance TEXT, gender TEXT, age INTEGER, emotional_core TEXT, emotional_trigger TEXT, emotional_wound TEXT, emotional_need TEXT, life_status TEXT NOT NULL DEFAULT 'alive', death_chapter INTEGER,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
        );

CREATE TABLE chase_debt (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id TEXT NOT NULL,
                debt_type TEXT NOT NULL,
                original_amount REAL NOT NULL DEFAULT 1.0,
                current_amount REAL NOT NULL DEFAULT 1.0,
                interest_rate REAL NOT NULL DEFAULT 0.1,
                source_chapter INTEGER NOT NULL,
                due_chapter INTEGER NOT NULL,
                override_contract_id INTEGER,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE chat_messages (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
            );

CREATE TABLE chat_sessions (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                title TEXT NOT NULL,
                context TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE collab_participants (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    user_name TEXT NOT NULL,
                    cursor_line INTEGER,
                    cursor_column INTEGER,
                    joined_at TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES collab_sessions(id) ON DELETE CASCADE,
                    UNIQUE(session_id, user_id)
                );

CREATE TABLE collab_sessions (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    chapter_id TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
                );

CREATE TABLE comment_messages (
            id TEXT PRIMARY KEY,
            thread_id TEXT NOT NULL,
            author_id TEXT NOT NULL,
            author_name TEXT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (thread_id) REFERENCES comment_threads(id) ON DELETE CASCADE
        );

CREATE TABLE comment_threads (
            id TEXT PRIMARY KEY,
            scene_id TEXT,
            chapter_id TEXT,
            version_id TEXT,
            anchor_type TEXT NOT NULL,
            from_pos INTEGER,
            to_pos INTEGER,
            selected_text TEXT,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL,
            resolved_at TEXT,
            FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE CASCADE,
            FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE,
            FOREIGN KEY (version_id) REFERENCES scene_versions(id) ON DELETE CASCADE
        );

CREATE TABLE conflict_escalations (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL REFERENCES stories(id),
                conflict_type TEXT NOT NULL,
                party_a_ids TEXT NOT NULL DEFAULT '[]',
                party_b_ids TEXT NOT NULL DEFAULT '[]',
                intensity_timeline_json TEXT NOT NULL DEFAULT '[]',
                current_intensity REAL NOT NULL DEFAULT 0.0,
                is_escalated INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id)
            );

CREATE TABLE continuation_training_reports (id TEXT PRIMARY KEY,task_id TEXT NOT NULL,book_title TEXT NOT NULL,source_kind TEXT NOT NULL,story_id TEXT NOT NULL,run_id TEXT,start_chapter INTEGER NOT NULL,context_chapters INTEGER NOT NULL,generated_chapter INTEGER,truth_content TEXT,scores_json TEXT,report_md TEXT NOT NULL,improvement_md TEXT,style_dna_applied INTEGER NOT NULL DEFAULT 0,created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')));

CREATE TABLE corpus_items (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                title TEXT NOT NULL,
                summary TEXT NOT NULL DEFAULT '',
                content TEXT NOT NULL DEFAULT '',
                source_url TEXT,
                source_name TEXT,
                tags TEXT NOT NULL DEFAULT '[]',
                file_path TEXT,
                file_name TEXT,
                mime_type TEXT,
                file_size INTEGER,
                file_hash TEXT,
                status TEXT NOT NULL DEFAULT 'raw',
                pinned INTEGER NOT NULL DEFAULT 0,
                distilled_json TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE corpus_links (
                id TEXT PRIMARY KEY,
                corpus_id TEXT NOT NULL,
                target_type TEXT NOT NULL,
                target_id TEXT NOT NULL,
                note TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (corpus_id) REFERENCES corpus_items(id) ON DELETE CASCADE
            );

CREATE TABLE custom_methodologies (
                id TEXT PRIMARY KEY,
                guidebook_id TEXT REFERENCES guidebooks(id) ON DELETE SET NULL,
                name TEXT NOT NULL,
                description TEXT,
                steps_json TEXT NOT NULL DEFAULT '[]',
                enabled INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            , patterns_json TEXT NOT NULL DEFAULT '[]', cheatsheet_json TEXT NOT NULL DEFAULT '{}');

CREATE TABLE drafts (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                chapter_number INTEGER NOT NULL,
                scene_id TEXT,
                version INTEGER NOT NULL DEFAULT 1,
                status TEXT NOT NULL DEFAULT 'draft',
                source TEXT NOT NULL DEFAULT 'write',
                content TEXT NOT NULL DEFAULT '',
                word_count INTEGER NOT NULL DEFAULT 0,
                model_used TEXT,
                cost REAL,
                metadata TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
                UNIQUE(story_id, chapter_number, version)
            );

CREATE TABLE editor_gate_records (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                chapter_number INTEGER NOT NULL,
                round INTEGER NOT NULL DEFAULT 1,
                outcome TEXT NOT NULL,
                verdict TEXT,
                score REAL,
                weighted REAL,
                dimension_scores_json TEXT,
                findings_json TEXT,
                source TEXT,
                created_at TEXT NOT NULL
            , run_id TEXT);

CREATE TABLE emotion_debts (
  id TEXT PRIMARY KEY,
  story_id TEXT NOT NULL,
  kind TEXT NOT NULL,
  source_ref TEXT,
  description TEXT,
  pressure REAL NOT NULL DEFAULT 0.5,
  due_chapter INTEGER,
  status TEXT NOT NULL DEFAULT 'open',
  created_at TEXT NOT NULL,
  FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE emotion_probe_log (
  id TEXT PRIMARY KEY,
  story_id TEXT NOT NULL,
  scene_id TEXT,
  beat_index INTEGER,
  probe TEXT NOT NULL,
  severity TEXT NOT NULL,
  passed INTEGER NOT NULL,
  detail_json TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE emotion_tensions (
  id TEXT PRIMARY KEY,
  story_id TEXT NOT NULL,
  source_character_id TEXT NOT NULL,
  target_character_id TEXT,
  tension_type TEXT NOT NULL,
  bond TEXT,
  reverse_bond TEXT,
  pressure REAL NOT NULL DEFAULT 0.5,
  accumulated_beats INTEGER NOT NULL DEFAULT 0,
  due_chapter INTEGER,
  status TEXT NOT NULL DEFAULT 'open',
  last_escalated_chapter INTEGER,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE entity_mentions (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                scene_id TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                start_pos INTEGER NOT NULL,
                end_pos INTEGER NOT NULL,
                mention_text TEXT NOT NULL,
                confidence REAL NOT NULL DEFAULT 1.0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE CASCADE,
                FOREIGN KEY (entity_id) REFERENCES kg_entities(id) ON DELETE CASCADE
            );

CREATE TABLE execution_graphs (
    id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,           -- 用户请求唯一标识
    story_id TEXT,                      -- 关联故事 ID
    user_input TEXT NOT NULL,           -- 原始用户输入
    root_intention_id TEXT,             -- 根意图节点 ID
    status TEXT NOT NULL,               -- 'building' | 'executing' | 'completed' | 'failed' | 'cancelled'
    plan_json TEXT,                     -- 生成的 ExecutionPlan JSON
    result_json TEXT,                   -- 执行结果 JSON
    created_at INTEGER NOT NULL,
    completed_at INTEGER,
    execution_time_ms INTEGER           -- 总执行时间
);

CREATE TABLE execution_nodes (
    id TEXT PRIMARY KEY,
    graph_id TEXT NOT NULL,
    intention_id TEXT,                  -- 关联意图（可为空，表示直接资产调用）
    asset_id TEXT,                      -- 关联资产（可为空，表示纯意图节点）
    status TEXT NOT NULL,                 -- 'discovered' | 'pending' | 'running' | 'completed' | 'failed' | 'skipped'
    parameters TEXT,                    -- JSON 参数
    depends_on TEXT,                    -- JSON 数组：依赖的 execution_node IDs
    outputs TEXT,                       -- JSON 执行输出
    discovered_from TEXT,               -- 发现来源：'synthesis' | 'ppr' | 'semantic' | 'output_heuristic' | 'llm_assisted'
    execution_time_ms INTEGER,
    created_at INTEGER NOT NULL,
    completed_at INTEGER,
    FOREIGN KEY (graph_id) REFERENCES execution_graphs(id) ON DELETE CASCADE,
    FOREIGN KEY (intention_id) REFERENCES intention_nodes(id) ON DELETE SET NULL,
    FOREIGN KEY (asset_id) REFERENCES asset_nodes(id) ON DELETE SET NULL
);

CREATE TABLE export_templates (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    format TEXT NOT NULL,
                    template_content TEXT NOT NULL,
                    is_builtin INTEGER NOT NULL DEFAULT 0,
                    is_user_created INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                );

CREATE TABLE feature_usage_logs (
                id TEXT PRIMARY KEY,
                feature_id TEXT NOT NULL,
                action TEXT NOT NULL,
                story_id TEXT,
                metadata TEXT,
                created_at TEXT NOT NULL
            );

CREATE TABLE foreshadowing_tracker (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    setup_scene_id TEXT,
                    payoff_scene_id TEXT,
                    status TEXT NOT NULL DEFAULT 'setup',
                    importance INTEGER,
                    created_at TEXT NOT NULL,
                    resolved_at TEXT
                , target_start_scene INTEGER, target_end_scene INTEGER, risk_signals TEXT, scope_type TEXT DEFAULT 'story', ledger_key TEXT, setup_event_id TEXT, payoff_event_id TEXT, risk_signals_score REAL DEFAULT 0.0, evidence TEXT, strength INTEGER DEFAULT 5, subtlety INTEGER DEFAULT 5, related_foreshadow_ids TEXT DEFAULT '[]');

CREATE TABLE genesis_runs (
                id TEXT PRIMARY KEY,
                story_id TEXT,
                session_id TEXT NOT NULL,
                premise TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                current_step TEXT,
                current_step_number INTEGER NOT NULL DEFAULT 0,
                total_steps INTEGER NOT NULL DEFAULT 7,
                steps_json TEXT NOT NULL DEFAULT '{}',
                error_message TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

CREATE TABLE genre_profiles (
                id TEXT PRIMARY KEY,
                genre_name TEXT NOT NULL UNIQUE,
                canonical_name TEXT NOT NULL,
                aliases_json TEXT,
                core_tone TEXT,
                pacing_strategy TEXT,
                anti_patterns_json TEXT,
                reference_tables_json TEXT,
                is_builtin INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            , typical_structure_json TEXT, reader_promise TEXT, recommended_style_dna_ids TEXT, recommended_methodology_id TEXT, recommended_skill_ids TEXT, min_quality_tier TEXT DEFAULT 'low');

CREATE TABLE guidebooks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL DEFAULT '未命名',
                author TEXT,
                subject TEXT,
                word_count INTEGER,
                file_format TEXT,
                file_hash TEXT UNIQUE,
                file_path TEXT,
                methodology_id TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                progress INTEGER NOT NULL DEFAULT 0,
                error TEXT,
                task_id TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            , merge_into_methodology_id TEXT);

CREATE TABLE ingest_jobs (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                resource_id TEXT,
                status TEXT NOT NULL,
                error_message TEXT,
                created_at TEXT NOT NULL,
                completed_at TEXT
            );

CREATE TABLE intention_asset_edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intention_id TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    edge_type TEXT NOT NULL,            -- 'has_intention' | 'triggered_by' | 'recommended'
    weight REAL NOT NULL DEFAULT 1.0,   -- 边权重（0-1）
    reason TEXT,                        -- 为什么建立这条边（LLM 解释或规则来源）
    cooccurrence_count INTEGER NOT NULL DEFAULT 1, -- 共现次数（用于动态更新）
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    FOREIGN KEY (intention_id) REFERENCES intention_nodes(id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES asset_nodes(id) ON DELETE CASCADE,
    UNIQUE(intention_id, asset_id, edge_type)
);

CREATE TABLE intention_nodes (
    id TEXT PRIMARY KEY,
    intent_type TEXT NOT NULL,          -- 'atomic' | 'compound' | 'synthetic'
    verb TEXT NOT NULL,                 -- 动作动词（如 generate, enhance, analyze）
    object TEXT NOT NULL,               -- 宾语对象（如 prose, style, character）
    description TEXT NOT NULL,          -- 自然语言描述
    embedding BLOB,                     -- 语义嵌入向量（JSON 数组）
    frequency INTEGER NOT NULL DEFAULT 1, -- 出现频率（用于 PPR 权重）
    created_at INTEGER NOT NULL,        -- Unix timestamp
    updated_at INTEGER NOT NULL         -- Unix timestamp
);

CREATE TABLE item_holdings (
    id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    item_name TEXT NOT NULL,
    item_entity_id TEXT,
    holder_name TEXT,
    holder_character_id TEXT,
    status TEXT NOT NULL DEFAULT 'held',
    acquired_chapter INTEGER,
    evidence TEXT,
    source_scene_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE kg_entities (
            id TEXT PRIMARY KEY,
            story_id TEXT NOT NULL,
            name TEXT NOT NULL,
            entity_type TEXT NOT NULL,      -- character/location/item/concept/event/organization
            attributes TEXT,                -- JSON
            embedding BLOB,                 -- 向量嵌入（可选）
            first_seen TEXT NOT NULL,
            last_updated TEXT NOT NULL,
            confidence_score REAL,          -- 置信度 (0-1)
            access_count INTEGER DEFAULT 0, -- 访问计数（遗忘曲线）
            last_accessed TEXT,             -- 最后访问时间
            is_archived INTEGER DEFAULT 0,  -- 归档状态
            archived_at TEXT,               -- 归档时间
            source TEXT DEFAULT 'user_created',
            is_auto_generated INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
        );

CREATE TABLE kg_relations (
            id TEXT PRIMARY KEY,
            story_id TEXT NOT NULL,
            source_id TEXT NOT NULL,
            target_id TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            strength REAL NOT NULL,         -- 0-1
            evidence TEXT,                  -- JSON: 场景ID列表
            first_seen TEXT NOT NULL,
            confidence_score REAL,          -- 置信度 (0-1)
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
            FOREIGN KEY (source_id) REFERENCES kg_entities(id) ON DELETE CASCADE,
            FOREIGN KEY (target_id) REFERENCES kg_entities(id) ON DELETE CASCADE
        );

CREATE TABLE llm_calls (
                id TEXT PRIMARY KEY,
                story_id TEXT,
                draft_id TEXT,
                revision_id TEXT,
                model_id TEXT NOT NULL,
                model_name TEXT,
                purpose TEXT NOT NULL,
                prompt_tokens INTEGER NOT NULL DEFAULT 0,
                completion_tokens INTEGER NOT NULL DEFAULT 0,
                total_tokens INTEGER NOT NULL DEFAULT 0,
                duration_ms INTEGER NOT NULL DEFAULT 0,
                success INTEGER NOT NULL DEFAULT 1,
                error_message TEXT,
                prompt_preview TEXT,
                metadata TEXT,
                created_at TEXT NOT NULL
            , task_type TEXT, quality_score REAL, latency_ms INTEGER, route_decision TEXT, audit_feedback TEXT);

CREATE TABLE mcp_server_configs (id TEXT PRIMARY KEY,name TEXT NOT NULL,config_json TEXT NOT NULL,enabled INTEGER NOT NULL DEFAULT 1,created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime')));

CREATE TABLE memory_items (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                category TEXT NOT NULL,
                subject TEXT,
                field TEXT,
                value TEXT,
                source_chapter INTEGER,
                confidence REAL NOT NULL DEFAULT 1.0,
                status TEXT NOT NULL DEFAULT 'active',
                updated_at TEXT NOT NULL, kg_entity_id TEXT REFERENCES kg_entities(id),
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE model_capability_profile (
            model_id              TEXT PRIMARY KEY,
            short_ttfb_ms_p50     INTEGER,
            short_ttfb_ms_p95     INTEGER,
            long_ttfb_ms_p50      INTEGER,
            long_ttfb_ms_p95      INTEGER,
            sustained_tps         REAL,
            short_output_tps      REAL,
            success_rate_24h      REAL,
            last_full_benchmark_at INTEGER,
            last_health_probe_at  INTEGER,
            benchmark_sample_count INTEGER NOT NULL DEFAULT 0,
            status                TEXT NOT NULL DEFAULT 'unknown',
            status_reason         TEXT,
            capability_score      REAL,
            speed_score           REAL,
            quality_score         REAL,
            created_at            INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
            updated_at            INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
        );

CREATE TABLE narrative_characters (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    role_type TEXT,
                    personality TEXT,
                    background TEXT,
                    goals TEXT,
                    appearance TEXT,
                    gender TEXT,
                    age INTEGER,
                    importance_score REAL,
                    source TEXT NOT NULL DEFAULT 'user_created',
                    source_ref_id TEXT,
                    status TEXT NOT NULL DEFAULT 'active',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
                );

CREATE TABLE narrative_chunks (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL REFERENCES stories(id),
                chapter_range_start INTEGER NOT NULL,
                chapter_range_end INTEGER NOT NULL,
                scene_ids TEXT NOT NULL DEFAULT '[]',
                event_ids TEXT NOT NULL DEFAULT '[]',
                text TEXT NOT NULL,
                chunk_type TEXT NOT NULL,
                is_boundary_start INTEGER NOT NULL DEFAULT 0,
                is_boundary_end INTEGER NOT NULL DEFAULT 0,
                thread_ids TEXT NOT NULL DEFAULT '[]',
                vector_id TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id)
            );

CREATE TABLE narrative_scenes (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    sequence_number INTEGER NOT NULL,
                    title TEXT,
                    summary TEXT,
                    dramatic_goal TEXT,
                    external_pressure TEXT,
                    conflict_type TEXT,
                    characters_present TEXT,
                    setting_location TEXT,
                    setting_time TEXT,
                    content TEXT,
                    key_events TEXT,
                    emotional_tone TEXT,
                    narrative_intensity REAL DEFAULT 0.0,
                    narrative_sentiment REAL DEFAULT 0.0,
                    narrative_event_types TEXT DEFAULT '[]',
                    act_number INTEGER DEFAULT 1,
                    position_in_act REAL DEFAULT 0.0,
                    source TEXT NOT NULL DEFAULT 'user_created',
                    source_ref_id TEXT,
                    status TEXT NOT NULL DEFAULT 'active',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
                );

CREATE TABLE narrative_structure_positions (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL REFERENCES stories(id),
                event_id TEXT NOT NULL REFERENCES narrative_events(id),
                act_number INTEGER NOT NULL,
                act_type TEXT NOT NULL,
                position_in_act REAL NOT NULL,
                dramatic_function TEXT NOT NULL,
                is_narrative_boundary INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id),
                FOREIGN KEY (event_id) REFERENCES narrative_events(id)
            );

CREATE TABLE narrative_world_buildings (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL UNIQUE,
                    concept TEXT NOT NULL,
                    rules TEXT,
                    history TEXT,
                    key_locations TEXT,
                    power_system TEXT,
                    source TEXT NOT NULL DEFAULT 'user_created',
                    source_ref_id TEXT,
                    status TEXT NOT NULL DEFAULT 'active',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
                );

CREATE TABLE novel_bootstrap_sessions (
                    id TEXT PRIMARY KEY,
                    story_id TEXT,
                    status TEXT NOT NULL DEFAULT 'in_progress',
                    current_step TEXT NOT NULL DEFAULT 'concept',
                    steps_completed INTEGER DEFAULT 0,
                    total_steps INTEGER DEFAULT 5,
                    error_message TEXT,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                );

CREATE TABLE oauth_accounts (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                provider TEXT NOT NULL,
                provider_account_id TEXT NOT NULL,
                access_token TEXT,
                refresh_token TEXT,
                expires_at TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(provider, provider_account_id)
            );

CREATE TABLE override_contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                story_id TEXT NOT NULL,
                chapter_number INTEGER NOT NULL,
                constraint_type TEXT NOT NULL,
                constraint_id TEXT NOT NULL,
                rationale_type TEXT NOT NULL,
                rationale_text TEXT NOT NULL,
                payback_plan TEXT NOT NULL,
                due_chapter INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                fulfilled_at TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE pending_reviews (
    id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    kind TEXT NOT NULL DEFAULT 'world_rule',
    subject TEXT NOT NULL,
    detail TEXT,
    source TEXT NOT NULL DEFAULT 'ingest',
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(story_id, kind, subject),
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE pending_vector_indexes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chapter_id TEXT NOT NULL UNIQUE,
                created_at INTEGER NOT NULL
            );

CREATE TABLE plan_templates (
                id TEXT PRIMARY KEY,
                trigger_patterns TEXT NOT NULL,
                plan_json TEXT NOT NULL,
                success_count INTEGER NOT NULL DEFAULT 0,
                failure_count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );

CREATE TABLE post_process_runs (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                chapter_number INTEGER NOT NULL,
                source_label TEXT NOT NULL,
                scope TEXT,
                status TEXT NOT NULL DEFAULT 'running',
                started_at TEXT NOT NULL,
                completed_at TEXT,
                error_message TEXT,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE post_process_steps (
                id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                step_key TEXT NOT NULL,
                step_label TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                critical INTEGER NOT NULL DEFAULT 0,
                log_output TEXT,
                error_message TEXT,
                started_at TEXT,
                completed_at TEXT,
                FOREIGN KEY (run_id) REFERENCES post_process_runs(id) ON DELETE CASCADE
            );

CREATE TABLE prompt_overrides (
            prompt_id           TEXT PRIMARY KEY,
            overridden_content  TEXT NOT NULL,
            updated_at          INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
        );

CREATE TABLE quality_debts (
    id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    scene_id TEXT,
    chapter_number INTEGER,
    source TEXT NOT NULL DEFAULT 'editor_qc',
    severity TEXT NOT NULL DEFAULT 'warning',
    detail TEXT NOT NULL,
    suggested_window TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(story_id, chapter_number, detail),
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE reader_resonance_reviews (
  id TEXT PRIMARY KEY,
  story_id TEXT NOT NULL,
  scene_id TEXT,
  chapter_number INTEGER,
  persona TEXT NOT NULL,
  scores_json TEXT NOT NULL,
  verdict TEXT NOT NULL,
  evidence_json TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE reference_books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            genre TEXT,
            word_count INTEGER,
            file_format TEXT,
            file_hash TEXT UNIQUE,
            file_path TEXT,
            world_setting TEXT,
            plot_summary TEXT,
            story_arc TEXT,
            analysis_status TEXT NOT NULL DEFAULT 'pending',
            analysis_progress INTEGER DEFAULT 0,
            analysis_error TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        , task_id TEXT, analyzed_structure_json TEXT);

CREATE TABLE reference_characters (
            id TEXT PRIMARY KEY,
            book_id TEXT NOT NULL,
            name TEXT NOT NULL,
            role_type TEXT,
            personality TEXT,
            appearance TEXT,
            relationships TEXT,
            key_scenes TEXT,
            importance_score REAL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES reference_books(id) ON DELETE CASCADE
        );

CREATE TABLE reference_scenes (
            id TEXT PRIMARY KEY,
            book_id TEXT NOT NULL,
            sequence_number INTEGER NOT NULL,
            title TEXT,
            summary TEXT,
            characters_present TEXT,
            key_events TEXT,
            conflict_type TEXT,
            emotional_tone TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES reference_books(id) ON DELETE CASCADE
        );

CREATE TABLE review_issues (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                scene_id TEXT,
                chapter_number INTEGER NOT NULL,
                severity TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT,
                description TEXT NOT NULL,
                evidence TEXT,
                fix_hint TEXT,
                blocking INTEGER NOT NULL DEFAULT 0,
                resolved INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
                FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE SET NULL
            );

CREATE TABLE reviews (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                draft_id TEXT NOT NULL,
                review_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                dimensions TEXT,
                issues TEXT,
                overall_score REAL,
                review_focus TEXT,
                model_used TEXT,
                cost REAL,
                metadata TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
                FOREIGN KEY (draft_id) REFERENCES drafts(id) ON DELETE CASCADE
            );

CREATE TABLE revisions (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                draft_id TEXT NOT NULL,
                revision_index INTEGER NOT NULL,
                revision_type TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                user_prompt TEXT,
                original_content TEXT NOT NULL,
                revised_content TEXT NOT NULL,
                word_count INTEGER NOT NULL DEFAULT 0,
                change_summary TEXT,
                model_used TEXT,
                cost REAL,
                metadata TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
                FOREIGN KEY (draft_id) REFERENCES drafts(id) ON DELETE CASCADE
            );

CREATE TABLE scene_annotations (
            id TEXT PRIMARY KEY,
            scene_id TEXT NOT NULL,
            story_id TEXT NOT NULL,
            content TEXT NOT NULL,
            annotation_type TEXT NOT NULL DEFAULT 'note',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            resolved_at TEXT,
            FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE CASCADE,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
        );

CREATE TABLE scene_character_actions (
                id TEXT PRIMARY KEY,
                scene_id TEXT NOT NULL,
                character_id TEXT NOT NULL,
                action_type TEXT,
                content TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE CASCADE,
                FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
            );

CREATE TABLE scene_characters (
                id TEXT PRIMARY KEY,
                scene_id TEXT NOT NULL,
                character_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE CASCADE,
                FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE,
                UNIQUE(scene_id, character_id)
            );

CREATE TABLE scene_commits (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                scene_id TEXT,
                chapter_id TEXT REFERENCES chapters(id) ON DELETE SET NULL,
                chapter_number INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                outline_snapshot_json TEXT,
                review_result_json TEXT,
                fulfillment_result_json TEXT,
                accepted_events_json TEXT,
                state_deltas_json TEXT,
                entity_deltas_json TEXT,
                summary_text TEXT,
                dominant_strand TEXT,
                projection_status_json TEXT,
                created_at TEXT NOT NULL, summary_source_hash TEXT,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
                FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE SET NULL
            );

CREATE TABLE scene_divider_nodes (
                id TEXT PRIMARY KEY,
                chapter_id TEXT NOT NULL,
                position INTEGER NOT NULL,
                scene_id TEXT NOT NULL,
                label TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE,
                FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE CASCADE,
                UNIQUE(chapter_id, position)
            );

CREATE TABLE scene_emotion_beats (
  id TEXT PRIMARY KEY,
  story_id TEXT NOT NULL,
  scene_id TEXT NOT NULL,
  beat_index INTEGER NOT NULL,
  from_json TEXT NOT NULL,
  to_json TEXT NOT NULL,
  trigger_event TEXT,
  appraisal_json TEXT,
  action_tendency TEXT,
  dialogue_policy_json TEXT,
  cost TEXT,
  carrier_weights_json TEXT NOT NULL,
  reader_target_json TEXT,
  scale REAL NOT NULL DEFAULT 0.8,
  event_kind TEXT,
  source_name TEXT,
  target_name TEXT,
  tension_id TEXT,
  debt_id TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
  FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE CASCADE
);

CREATE TABLE scene_outcomes (
    scene_id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    chapter_number INTEGER NOT NULL,
    outcome TEXT NOT NULL,
    state_delta_json TEXT NOT NULL,
    emotion_json TEXT,
    open_question TEXT NOT NULL,
    contract_misses_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE scene_versions (
            id TEXT PRIMARY KEY,
            scene_id TEXT NOT NULL,
            version_number INTEGER NOT NULL,
            title TEXT,
            content TEXT,
            dramatic_goal TEXT,
            external_pressure TEXT,
            conflict_type TEXT,
            characters_present TEXT,
            character_conflicts TEXT,
            setting_location TEXT,
            setting_time TEXT,
            setting_atmosphere TEXT,
            word_count INTEGER,
            change_summary TEXT NOT NULL,
            created_by TEXT NOT NULL,
            model_used TEXT,
            confidence_score REAL,
            previous_version_id TEXT,
            superseded_by TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (scene_id) REFERENCES scenes(id) ON DELETE CASCADE,
            FOREIGN KEY (previous_version_id) REFERENCES scene_versions(id) ON DELETE SET NULL,
            FOREIGN KEY (superseded_by) REFERENCES scene_versions(id) ON DELETE SET NULL
        );

CREATE TABLE scenes (
            id TEXT PRIMARY KEY,
            story_id TEXT NOT NULL,
            sequence_number INTEGER NOT NULL,
            title TEXT,
            dramatic_goal TEXT,             -- 戏剧目标：这个场景要完成什么
            external_pressure TEXT,         -- 外部压迫：环境/反派/事件对角色的压迫
            conflict_type TEXT,             -- 冲突类型
            characters_present TEXT,        -- JSON: [character_id, ...]
            character_conflicts TEXT,       -- JSON: [{a, b, nature, stakes}, ...]
            setting_location TEXT,
            setting_time TEXT,
            setting_atmosphere TEXT,
            content TEXT,
            previous_scene_id TEXT,
            next_scene_id TEXT,
            chapter_id TEXT,                -- 1:N Chapter↔Scene 关联
            model_used TEXT,
            cost REAL,
            source TEXT DEFAULT 'user_created',
            is_auto_generated INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL, confidence_score REAL, execution_stage TEXT DEFAULT 'drafting', outline_content TEXT, draft_content TEXT, style_blend_override TEXT, foreshadowing_ids TEXT, narrative_intensity REAL DEFAULT 0.5, narrative_sentiment REAL DEFAULT 0.0, narrative_event_types TEXT DEFAULT '[]', narrative_preceding_scene_id TEXT, narrative_following_scene_id TEXT, act_number INTEGER DEFAULT 1, position_in_act INTEGER DEFAULT 1,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
            FOREIGN KEY (previous_scene_id) REFERENCES scenes(id) ON DELETE SET NULL,
            FOREIGN KEY (next_scene_id) REFERENCES scenes(id) ON DELETE SET NULL,
            FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE SET NULL,
            UNIQUE(story_id, sequence_number)
        );

CREATE TABLE schema_migrations (
            version INTEGER PRIMARY KEY,
            applied_at INTEGER NOT NULL
        , checksum TEXT);

CREATE TABLE sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                token TEXT NOT NULL UNIQUE,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

CREATE TABLE settings (
            id TEXT PRIMARY KEY,
            story_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            location_type TEXT,             -- city/building/nature/...
            sensory_details TEXT,           -- JSON: 感官细节
            significance TEXT,              -- 在故事中的重要性
            created_at TEXT NOT NULL,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
        );

CREATE TABLE stories (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            genre TEXT,
            tone TEXT,
            pacing TEXT,
            style_dna_id TEXT,
            reference_book_id TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        , methodology_id TEXT, methodology_step INTEGER, genre_profile_id TEXT, logline TEXT, strategy_json TEXT, asset_history_json TEXT, story_format TEXT NOT NULL DEFAULT 'novel', production_constraints TEXT);

CREATE TABLE story_chapter_sequences (
  story_id TEXT PRIMARY KEY,
  next_chapter INTEGER NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE story_checkpoints (
    id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    chapter_number INTEGER NOT NULL,
    snapshot_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(story_id, chapter_number),
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE story_contracts (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                contract_type TEXT NOT NULL,
                contract_json TEXT NOT NULL,
                version INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE story_emotion_contracts (
  story_id TEXT PRIMARY KEY,
  core_question TEXT,
  reader_promise TEXT,
  palette_json TEXT NOT NULL DEFAULT '{}',
  ending_residue TEXT,
  forbidden_json TEXT NOT NULL DEFAULT '[]',
  peak_budget INTEGER NOT NULL DEFAULT 1,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE story_material_staleness (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                from_chapter INTEGER NOT NULL,
                reason TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(story_id, kind)
            );

CREATE TABLE story_metadata (
                story_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (story_id, key),
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE story_outlines (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                structure_json TEXT,
                act_count INTEGER DEFAULT 3,
                total_scenes_estimate INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL, analyzed_structure_json TEXT, source TEXT,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE story_resource_leases (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                resource TEXT NOT NULL,
                owner_run_id TEXT,
                owner_task_id TEXT,
                acquired_at TEXT NOT NULL,
                heartbeat_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                UNIQUE(story_id, resource),
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE story_runtime_states (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL UNIQUE,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
            );

CREATE TABLE story_segment_summaries (
    id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    level TEXT NOT NULL DEFAULT 'segment',
    segment_index INTEGER NOT NULL,
    start_chapter INTEGER,
    end_chapter INTEGER,
    summary TEXT NOT NULL,
    source TEXT NOT NULL DEFAULT 'llm',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(story_id, level, segment_index),
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE story_style_configs (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                name TEXT NOT NULL DEFAULT '默认混合',
                blend_json TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

CREATE TABLE story_summaries (
            id TEXT PRIMARY KEY,
            story_id TEXT NOT NULL,
            summary_type TEXT NOT NULL DEFAULT 'knowledge_distillation',
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
        );

CREATE TABLE story_timeline_events (
    id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    chapter_number INTEGER,
    scene_id TEXT,
    sequence_number INTEGER,
    objective_fact TEXT NOT NULL,
    reader_knowledge TEXT,
    reveal_status TEXT NOT NULL DEFAULT 'hidden',
    reveal_chapter INTEGER,
    participants TEXT NOT NULL DEFAULT '[]',
    source TEXT NOT NULL DEFAULT 'ingest',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE studio_configs (
            id TEXT PRIMARY KEY,
            story_id TEXT NOT NULL UNIQUE,
            pen_name TEXT,
            llm_config TEXT,                -- JSON: LLM配置
            ui_config TEXT,                 -- JSON: UI配置
            agent_bots TEXT,                -- JSON: Agent Bot配置
            frontstage_theme TEXT,          -- CSS内容
            backstage_theme TEXT,           -- CSS内容
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
        );

CREATE TABLE style_dnas (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    author TEXT,
                    dna_json TEXT NOT NULL,
                    is_builtin INTEGER NOT NULL DEFAULT 0,
                    is_user_created INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                );

CREATE TABLE style_preferences (
    id TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    pattern TEXT NOT NULL,
    evidence TEXT,
    source TEXT NOT NULL DEFAULT 'user_edit',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(story_id, pattern),
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
);

CREATE TABLE style_snapshots (
                id TEXT PRIMARY KEY,
                story_id TEXT NOT NULL,
                chapter_number INTEGER,
                scene_number INTEGER,
                sentence_length REAL NOT NULL,
                dialogue_ratio REAL NOT NULL,
                metaphor_density REAL NOT NULL,
                inner_monologue_ratio REAL NOT NULL,
                emotion_density REAL NOT NULL,
                rhythm_score REAL NOT NULL,
                computed_at TEXT NOT NULL
            );

CREATE TABLE subscriptions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    tier TEXT NOT NULL DEFAULT 'free',
                    status TEXT NOT NULL DEFAULT 'active',
                    started_at TEXT NOT NULL,
                    expires_at TEXT,
                    payment_provider TEXT,
                    payment_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                , real_user_id TEXT REFERENCES users(id));

CREATE TABLE task_logs (
                    id TEXT PRIMARY KEY,
                    task_id TEXT NOT NULL,
                    log_level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
                );

CREATE TABLE tasks (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    task_type TEXT NOT NULL DEFAULT 'custom',
                    schedule_type TEXT NOT NULL DEFAULT 'once',
                    cron_pattern TEXT,
                    payload TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    progress INTEGER NOT NULL DEFAULT 0,
                    result TEXT,
                    error_message TEXT,
                    max_retries INTEGER NOT NULL DEFAULT 3,
                    retry_count INTEGER NOT NULL DEFAULT 0,
                    enabled INTEGER NOT NULL DEFAULT 1,
                    last_run_at TEXT,
                    next_run_at TEXT,
                    last_heartbeat_at TEXT,
                    heartbeat_timeout_seconds INTEGER NOT NULL DEFAULT 300,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

CREATE TABLE text_annotations (
            id TEXT PRIMARY KEY,
            story_id TEXT NOT NULL,
            scene_id TEXT,
            chapter_id TEXT,
            content TEXT NOT NULL,
            annotation_type TEXT NOT NULL DEFAULT 'note',
            from_pos INTEGER NOT NULL,
            to_pos INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            resolved_at TEXT, metadata TEXT, severity TEXT NOT NULL DEFAULT 'medium',
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
        );

CREATE TABLE user_feedback_log (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    scene_id TEXT,
                    chapter_id TEXT,
                    feedback_type TEXT NOT NULL,    -- accept / reject / modify
                    agent_type TEXT,                -- writer / inspector / etc
                    original_ai_text TEXT,          -- AI 生成的原始文本
                    final_text TEXT,                -- 用户最终接受的文本
                    ai_score REAL,                  -- AI 自评分数
                    user_satisfaction INTEGER,      -- 用户满意度 1-5（如提供）
                    metadata TEXT,                  -- JSON: 额外上下文
                    created_at TEXT NOT NULL
                );

CREATE TABLE user_preferences (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    preference_type TEXT,
                    preference_key TEXT,
                    preference_value TEXT,
                    confidence REAL,
                    evidence_count INTEGER,
                    updated_at TEXT
                );

CREATE TABLE users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                display_name TEXT,
                avatar_url TEXT,
                is_local_user INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

CREATE TABLE workflow_instances (
                id TEXT PRIMARY KEY,
                workflow_id TEXT NOT NULL,
                story_id TEXT NOT NULL,
                status TEXT NOT NULL,
                instance_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

CREATE TABLE world_buildings (
            id TEXT PRIMARY KEY,
            story_id TEXT NOT NULL UNIQUE,
            concept TEXT NOT NULL,          -- 宏观世界观概念
            rules TEXT,                     -- JSON: 世界规则列表
            history TEXT,
            cultures TEXT,                  -- JSON: 文化设定
            source TEXT DEFAULT 'user_created',
            is_auto_generated INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
        );

CREATE TABLE world_rules (
            id TEXT PRIMARY KEY,
            world_building_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            rule_type TEXT,                 -- magic/technology/social/...
            importance INTEGER,             -- 1-10
            created_at TEXT NOT NULL,
            FOREIGN KEY (world_building_id) REFERENCES world_buildings(id) ON DELETE CASCADE
        );

CREATE TABLE writing_styles (
            id TEXT PRIMARY KEY,
            story_id TEXT NOT NULL UNIQUE,
            name TEXT,
            description TEXT,
            tone TEXT,
            pacing TEXT,
            vocabulary_level TEXT,
            sentence_structure TEXT,
            custom_rules TEXT,              -- JSON: 自定义规则
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE
        );

CREATE INDEX idx_agency_activity_log_created ON agency_activity_log(created_at);

CREATE INDEX idx_agency_activity_log_run ON agency_activity_log(run_id);

CREATE INDEX idx_agency_board_run_key ON agency_board_items(run_id, zone, key);

CREATE INDEX idx_agency_board_run_zone ON agency_board_items(run_id, zone);

CREATE INDEX idx_agency_board_story_time ON agency_board_items(story_id, created_at);

CREATE INDEX idx_agency_chat_messages_session
                ON agency_chat_messages(session_id, created_at);

CREATE INDEX idx_agency_chat_sessions_story
                ON agency_chat_sessions(story_id, updated_at);

CREATE INDEX idx_agency_checkpoints_run ON agency_checkpoints(run_id, created_at);

CREATE INDEX idx_agency_checkpoints_story ON agency_checkpoints(story_id, created_at);

CREATE INDEX idx_agency_messages_run ON agency_messages(run_id, to_role);

CREATE UNIQUE INDEX idx_agency_runs_one_active_per_lane
  ON agency_runs(story_id, lane)
  WHERE status IN ('pending', 'running') AND lane <> 'write';

CREATE INDEX idx_agency_runs_status ON agency_runs(status);

CREATE INDEX idx_agency_runs_story ON agency_runs(story_id);

CREATE INDEX idx_agency_sessions_run ON agency_sessions(run_id, created_at);

CREATE INDEX idx_agency_sessions_story ON agency_sessions(story_id, created_at);

CREATE INDEX idx_agency_tasks_parent
                ON agency_agent_tasks(parent_task_id);

CREATE INDEX idx_agency_tasks_run
                ON agency_agent_tasks(run_id, created_at);

CREATE INDEX idx_agency_tasks_story_status
                ON agency_agent_tasks(story_id, status, heartbeat_at);

CREATE INDEX idx_ai_operations_chapter ON ai_operations(chapter_id);

CREATE INDEX idx_ai_operations_created ON ai_operations(created_at);

CREATE INDEX idx_ai_operations_scene ON ai_operations(scene_id);

CREATE INDEX idx_ai_operations_story ON ai_operations(story_id);

CREATE INDEX idx_ai_operations_type ON ai_operations(operation_type);

CREATE INDEX idx_asset_asset_edges_source ON asset_asset_edges(source_asset_id);

CREATE INDEX idx_asset_asset_edges_target ON asset_asset_edges(target_asset_id);

CREATE INDEX idx_asset_asset_edges_type ON asset_asset_edges(edge_type);

CREATE INDEX idx_asset_nodes_capability ON asset_nodes(capability_id);

CREATE INDEX idx_asset_nodes_type ON asset_nodes(asset_type);

CREATE INDEX idx_beat_technique_story_scene ON beat_technique_log(story_id, scene_id);

CREATE INDEX idx_beat_technique_story_time ON beat_technique_log(story_id, created_at);

CREATE INDEX idx_blueprints_chapter ON blueprints(story_id, chapter_number);

CREATE INDEX idx_blueprints_story ON blueprints(story_id);

CREATE INDEX idx_bootstrap_story ON novel_bootstrap_sessions(story_id);

CREATE INDEX idx_capability_score
            ON model_capability_profile(capability_score);

CREATE INDEX idx_capability_status
            ON model_capability_profile(status);

CREATE INDEX idx_cascade_impacts_story ON cascade_impacts(story_id, decision, created_at DESC);

CREATE INDEX idx_cascade_impacts_target ON cascade_impacts(target_scene_id);

CREATE INDEX idx_change_tracks_chapter ON change_tracks(chapter_id);

CREATE INDEX idx_change_tracks_scene ON change_tracks(scene_id);

CREATE INDEX idx_change_tracks_status ON change_tracks(status);

CREATE INDEX idx_chapters_number ON chapters(story_id, chapter_number);

CREATE INDEX idx_chapters_story ON chapters(story_id);

CREATE INDEX idx_char_rel_source ON character_relationships(source_character_id);

CREATE INDEX idx_char_rel_story ON character_relationships(story_id);

CREATE INDEX idx_char_rel_triple ON character_relationships(story_id, source_character_id, target_character_id);

CREATE INDEX idx_character_aliases_character
    ON character_aliases(character_id);

CREATE UNIQUE INDEX idx_character_aliases_unique
    ON character_aliases(story_id, alias);

CREATE INDEX idx_character_emotion_states_character
  ON character_emotion_states(story_id, character_id, chapter_number);

CREATE INDEX idx_character_emotion_states_story
  ON character_emotion_states(story_id, chapter_number);

CREATE INDEX idx_character_knowledge_log_char ON character_knowledge_log(story_id, character_id, chapter_number);

CREATE INDEX idx_character_names_story
    ON character_names (story_id);

CREATE INDEX idx_character_states_character ON character_states(character_id);

CREATE INDEX idx_character_states_story ON character_states(story_id);

CREATE INDEX idx_characters_story ON characters(story_id);

CREATE INDEX idx_characters_story_name ON characters(story_id, name);

CREATE INDEX idx_chase_debt_status ON chase_debt(story_id, status);

CREATE INDEX idx_chase_debt_story ON chase_debt(story_id);

CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);

CREATE INDEX idx_chat_sessions_story ON chat_sessions(story_id);

CREATE INDEX idx_collab_participants_session ON collab_participants(session_id);

CREATE INDEX idx_collab_sessions_story ON collab_sessions(story_id);

CREATE INDEX idx_comment_messages_thread ON comment_messages(thread_id);

CREATE INDEX idx_comment_threads_chapter ON comment_threads(chapter_id);

CREATE INDEX idx_comment_threads_scene ON comment_threads(scene_id);

CREATE INDEX idx_conflict_escalations_story ON conflict_escalations(story_id);

CREATE INDEX idx_conflict_escalations_type ON conflict_escalations(conflict_type);

CREATE INDEX idx_corpus_links_corpus
                ON corpus_links(corpus_id);

CREATE INDEX idx_corpus_links_target
                ON corpus_links(target_type, target_id);

CREATE UNIQUE INDEX idx_corpus_story_hash
                ON corpus_items(story_id, file_hash) WHERE file_hash IS NOT NULL;

CREATE INDEX idx_corpus_story_kind
                ON corpus_items(story_id, kind, created_at);

CREATE INDEX idx_custom_methodologies_guidebook
                ON custom_methodologies(guidebook_id);

CREATE INDEX idx_director_actions_status
                ON agency_director_actions(status, created_at);

CREATE INDEX idx_director_actions_story
                ON agency_director_actions(story_id, created_at);

CREATE INDEX idx_drafts_finalized ON drafts(story_id, chapter_number, status);

CREATE INDEX idx_drafts_status ON drafts(status);

CREATE INDEX idx_drafts_story_chapter ON drafts(story_id, chapter_number);

CREATE INDEX idx_drafts_story_scene ON drafts(story_id, scene_id);

CREATE INDEX idx_editor_gate_records_run ON editor_gate_records(run_id, chapter_number, created_at DESC);

CREATE INDEX idx_editor_gate_records_story_chapter ON editor_gate_records(story_id, chapter_number);

CREATE INDEX idx_emotion_debts_story
  ON emotion_debts(story_id, status, due_chapter);

CREATE INDEX idx_emotion_probe_story
  ON emotion_probe_log(story_id, scene_id, probe);

CREATE INDEX idx_emotion_tensions_story
  ON emotion_tensions(story_id, status, due_chapter);

CREATE INDEX idx_execution_graphs_request ON execution_graphs(request_id);

CREATE INDEX idx_execution_graphs_status ON execution_graphs(status);

CREATE INDEX idx_execution_graphs_story ON execution_graphs(story_id);

CREATE INDEX idx_execution_nodes_asset ON execution_nodes(asset_id);

CREATE INDEX idx_execution_nodes_graph ON execution_nodes(graph_id);

CREATE INDEX idx_execution_nodes_intention ON execution_nodes(intention_id);

CREATE INDEX idx_execution_nodes_status ON execution_nodes(status);

CREATE INDEX idx_export_templates_builtin ON export_templates(is_builtin);

CREATE INDEX idx_export_templates_format ON export_templates(format);

CREATE INDEX idx_feature_usage_feature ON feature_usage_logs(feature_id, created_at);

CREATE INDEX idx_feature_usage_story ON feature_usage_logs(story_id, created_at);

CREATE INDEX idx_feedback_created ON user_feedback_log(created_at);

CREATE INDEX idx_feedback_story ON user_feedback_log(story_id);

CREATE INDEX idx_feedback_type ON user_feedback_log(feedback_type);

CREATE UNIQUE INDEX idx_foreshadowing_ledger_key ON foreshadowing_tracker(ledger_key);

CREATE INDEX idx_foreshadowing_status ON foreshadowing_tracker(status);

CREATE INDEX idx_foreshadowing_story ON foreshadowing_tracker(story_id);

CREATE INDEX idx_genesis_runs_session ON genesis_runs(session_id);

CREATE INDEX idx_genesis_runs_status ON genesis_runs(status);

CREATE INDEX idx_genesis_runs_story ON genesis_runs(story_id);

CREATE INDEX idx_genre_profiles_canonical ON genre_profiles(canonical_name);

CREATE INDEX idx_ingest_jobs_status ON ingest_jobs(story_id, status);

CREATE INDEX idx_ingest_jobs_story ON ingest_jobs(story_id, created_at);

CREATE INDEX idx_intention_asset_edges_asset ON intention_asset_edges(asset_id);

CREATE INDEX idx_intention_asset_edges_intention ON intention_asset_edges(intention_id);

CREATE INDEX idx_intention_asset_edges_type ON intention_asset_edges(edge_type);

CREATE INDEX idx_intention_nodes_object ON intention_nodes(object);

CREATE INDEX idx_intention_nodes_type ON intention_nodes(intent_type);

CREATE INDEX idx_intention_nodes_verb ON intention_nodes(verb);

CREATE UNIQUE INDEX idx_item_holdings_story_item ON item_holdings(story_id, item_name);

CREATE INDEX idx_kg_entities_archived ON kg_entities(is_archived);

CREATE INDEX idx_kg_entities_story ON kg_entities(story_id);

CREATE INDEX idx_kg_entities_type ON kg_entities(entity_type);

CREATE INDEX idx_kg_relations_source ON kg_relations(source_id);

CREATE INDEX idx_kg_relations_story ON kg_relations(story_id);

CREATE INDEX idx_kg_relations_target ON kg_relations(target_id);

CREATE INDEX idx_kg_relations_type ON kg_relations(relation_type);

CREATE INDEX idx_llm_calls_model ON llm_calls(model_id);

CREATE INDEX idx_llm_calls_model_time ON llm_calls(model_id, created_at);

CREATE INDEX idx_llm_calls_purpose ON llm_calls(purpose);

CREATE INDEX idx_llm_calls_story ON llm_calls(story_id);

CREATE INDEX idx_llm_calls_story_time ON llm_calls(story_id, created_at);

CREATE INDEX idx_llm_calls_time ON llm_calls(created_at);

CREATE INDEX idx_material_staleness_story ON story_material_staleness(story_id);

CREATE INDEX idx_memory_items_category ON memory_items(story_id, category);

CREATE INDEX idx_memory_items_kg_entity ON memory_items(kg_entity_id);

CREATE INDEX idx_memory_items_status ON memory_items(story_id, status);

CREATE INDEX idx_memory_items_story ON memory_items(story_id);

CREATE INDEX idx_mentions_entity ON entity_mentions(entity_id);

CREATE INDEX idx_mentions_scene ON entity_mentions(scene_id);

CREATE INDEX idx_mentions_story ON entity_mentions(story_id);

CREATE INDEX idx_narrative_chars_source ON narrative_characters(source);

CREATE INDEX idx_narrative_chars_story ON narrative_characters(story_id);

CREATE INDEX idx_narrative_chunks_boundary ON narrative_chunks(is_boundary_start, is_boundary_end);

CREATE INDEX idx_narrative_chunks_story ON narrative_chunks(story_id);

CREATE INDEX idx_narrative_chunks_type ON narrative_chunks(chunk_type);

CREATE INDEX idx_narrative_scenes_source ON narrative_scenes(source);

CREATE INDEX idx_narrative_scenes_story ON narrative_scenes(story_id);

CREATE INDEX idx_narrative_structure_positions_boundary ON narrative_structure_positions(is_narrative_boundary);

CREATE INDEX idx_narrative_structure_positions_story ON narrative_structure_positions(story_id);

CREATE INDEX idx_narrative_wb_story ON narrative_world_buildings(story_id);

CREATE INDEX idx_oauth_accounts_provider ON oauth_accounts(provider, provider_account_id);

CREATE INDEX idx_oauth_accounts_user ON oauth_accounts(user_id);

CREATE INDEX idx_override_contracts_status ON override_contracts(story_id, status);

CREATE INDEX idx_override_contracts_story ON override_contracts(story_id);

CREATE INDEX idx_pending_reviews_story
    ON pending_reviews(story_id, status);

CREATE INDEX idx_pending_vector_chapter ON pending_vector_indexes(chapter_id);

CREATE INDEX idx_plan_templates_patterns ON plan_templates(trigger_patterns);

CREATE INDEX idx_post_process_runs_chapter ON post_process_runs(story_id, chapter_number);

CREATE INDEX idx_post_process_runs_story ON post_process_runs(story_id);

CREATE INDEX idx_post_process_steps_run ON post_process_steps(run_id);

CREATE INDEX idx_prompt_overrides_updated
            ON prompt_overrides(updated_at);

CREATE INDEX idx_quality_debts_story
    ON quality_debts(story_id, status, created_at DESC);

CREATE INDEX idx_reader_resonance_story
  ON reader_resonance_reviews(story_id, chapter_number);

CREATE UNIQUE INDEX idx_reading_power_chapter ON chapter_reading_power(story_id, chapter_number);

CREATE INDEX idx_reading_power_story ON chapter_reading_power(story_id);

CREATE INDEX idx_ref_books_hash ON reference_books(file_hash);

CREATE INDEX idx_ref_books_status ON reference_books(analysis_status);

CREATE INDEX idx_ref_books_task ON reference_books(task_id);

CREATE INDEX idx_ref_characters_book ON reference_characters(book_id);

CREATE INDEX idx_ref_scenes_book ON reference_scenes(book_id);

CREATE INDEX idx_review_issues_blocking ON review_issues(story_id, blocking);

CREATE INDEX idx_review_issues_severity ON review_issues(story_id, severity);

CREATE INDEX idx_review_issues_story ON review_issues(story_id);

CREATE INDEX idx_reviews_draft ON reviews(draft_id);

CREATE INDEX idx_reviews_story ON reviews(story_id);

CREATE INDEX idx_revisions_draft ON revisions(draft_id);

CREATE INDEX idx_revisions_story ON revisions(story_id);

CREATE INDEX idx_scene_annotations_resolved ON scene_annotations(resolved_at);

CREATE INDEX idx_scene_annotations_scene ON scene_annotations(scene_id);

CREATE INDEX idx_scene_annotations_story ON scene_annotations(story_id);

CREATE INDEX idx_scene_character_actions_character ON scene_character_actions(character_id);

CREATE INDEX idx_scene_character_actions_scene ON scene_character_actions(scene_id);

CREATE INDEX idx_scene_characters_character ON scene_characters(character_id);

CREATE INDEX idx_scene_characters_scene ON scene_characters(scene_id);

CREATE UNIQUE INDEX idx_scene_commits_number ON scene_commits(story_id, chapter_number);

CREATE INDEX idx_scene_commits_scene ON scene_commits(scene_id);

CREATE INDEX idx_scene_commits_story ON scene_commits(story_id);

CREATE INDEX idx_scene_divider_chapter ON scene_divider_nodes(chapter_id);

CREATE INDEX idx_scene_emotion_beats_scene
  ON scene_emotion_beats(scene_id, beat_index);

CREATE INDEX idx_scene_emotion_beats_story
  ON scene_emotion_beats(story_id, created_at);

CREATE INDEX idx_scene_outcomes_story
    ON scene_outcomes (story_id, chapter_number DESC);

CREATE INDEX idx_scene_versions_scene ON scene_versions(scene_id);

CREATE INDEX idx_scenes_next ON scenes(next_scene_id);

CREATE INDEX idx_scenes_prev ON scenes(previous_scene_id);

CREATE INDEX idx_scenes_sequence ON scenes(story_id, sequence_number);

CREATE INDEX idx_scenes_story ON scenes(story_id);

CREATE INDEX idx_sessions_token ON sessions(token);

CREATE INDEX idx_sessions_user ON sessions(user_id);

CREATE INDEX idx_settings_story ON settings(story_id);

CREATE INDEX idx_story_checkpoints_story
    ON story_checkpoints(story_id, chapter_number DESC);

CREATE INDEX idx_story_contracts_story ON story_contracts(story_id);

CREATE INDEX idx_story_contracts_type ON story_contracts(story_id, contract_type);

CREATE INDEX idx_story_leases_expiry
                ON story_resource_leases(expires_at);

CREATE INDEX idx_story_metadata_story ON story_metadata(story_id);

CREATE INDEX idx_story_outlines_story ON story_outlines(story_id);

CREATE INDEX idx_story_runtime_states_story ON story_runtime_states(story_id);

CREATE INDEX idx_story_segment_summaries_story
    ON story_segment_summaries(story_id, level, segment_index);

CREATE INDEX idx_story_style_configs_active ON story_style_configs(story_id, is_active);

CREATE INDEX idx_story_style_configs_story ON story_style_configs(story_id);

CREATE INDEX idx_story_summaries_story ON story_summaries(story_id);

CREATE INDEX idx_story_summaries_type ON story_summaries(story_id, summary_type);

CREATE INDEX idx_story_timeline_events_reveal ON story_timeline_events(story_id, reveal_status);

CREATE INDEX idx_story_timeline_events_story ON story_timeline_events(story_id, sequence_number);

CREATE INDEX idx_studio_configs_story ON studio_configs(story_id);

CREATE INDEX idx_style_dnas_builtin ON style_dnas(is_builtin);

CREATE INDEX idx_style_preferences_story
    ON style_preferences(story_id, status);

CREATE INDEX idx_style_snapshots_story ON style_snapshots(story_id);

CREATE INDEX idx_style_snapshots_story_chapter ON style_snapshots(story_id, chapter_number);

CREATE INDEX idx_subscriptions_tier ON subscriptions(tier);

CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);

CREATE INDEX idx_task_logs_task ON task_logs(task_id);

CREATE INDEX idx_tasks_enabled ON tasks(enabled);

CREATE INDEX idx_tasks_next_run ON tasks(next_run_at);

CREATE INDEX idx_tasks_status ON tasks(status);

CREATE INDEX idx_tasks_type ON tasks(task_type);

CREATE INDEX idx_text_annotations_chapter ON text_annotations(chapter_id);

CREATE INDEX idx_text_annotations_resolved ON text_annotations(resolved_at);

CREATE INDEX idx_text_annotations_scene ON text_annotations(scene_id);

CREATE INDEX idx_text_annotations_story ON text_annotations(story_id);

CREATE INDEX idx_training_reports_book ON continuation_training_reports(book_title, created_at DESC);

CREATE INDEX idx_usage_logs_created ON ai_usage_logs(created_at);

CREATE INDEX idx_usage_logs_user ON ai_usage_logs(user_id);

CREATE INDEX idx_user_preferences_story ON user_preferences(story_id);

CREATE INDEX idx_workflow_instances_status ON workflow_instances(status);

CREATE INDEX idx_workflow_instances_story ON workflow_instances(story_id);

CREATE INDEX idx_workflow_instances_workflow ON workflow_instances(workflow_id);

CREATE INDEX idx_world_buildings_story ON world_buildings(story_id);

CREATE INDEX idx_world_rules_wb ON world_rules(world_building_id);

CREATE INDEX idx_writing_styles_story ON writing_styles(story_id);

CREATE VIEW story_memory_facts AS
SELECT
  id,
  story_id,
  'kg_entity' AS record_kind,
  entity_type AS category,
  name AS subject,
  NULL AS field,
  COALESCE(json_extract(attributes, '$.description'), '') AS value,
  NULL AS source_chapter,
  COALESCE(confidence_score, 1.0) AS confidence,
  CASE WHEN is_archived = 1 THEN 'archived' ELSE 'active' END AS status,
  last_updated AS updated_at,
  id AS kg_entity_id,
  NULL AS memory_item_id
FROM kg_entities
UNION ALL
SELECT
  id,
  story_id,
  'memory_item' AS record_kind,
  category,
  subject,
  field,
  COALESCE(value, ''),
  source_chapter,
  confidence,
  status,
  updated_at,
  kg_entity_id,
  id AS memory_item_id
FROM memory_items;

CREATE TRIGGER trg_agency_agent_tasks_status_insert BEFORE INSERT ON agency_agent_tasks FOR EACH ROW WHEN NEW.status NOT IN ('queued','running','waiting','cancelling','completed','failed','cancelled','stale') BEGIN SELECT RAISE(ABORT, 'invalid agency_agent_tasks.status'); END;

CREATE TRIGGER trg_agency_agent_tasks_status_update BEFORE UPDATE OF status ON agency_agent_tasks FOR EACH ROW WHEN NEW.status NOT IN ('queued','running','waiting','cancelling','completed','failed','cancelled','stale') BEGIN SELECT RAISE(ABORT, 'invalid agency_agent_tasks.status'); END;

CREATE TRIGGER trg_agency_chat_messages_status_insert BEFORE INSERT ON agency_chat_messages FOR EACH ROW WHEN NEW.status NOT IN ('pending','thinking','acting','waiting','done','failed','cancelled','degraded') BEGIN SELECT RAISE(ABORT, 'invalid agency_chat_messages.status'); END;

CREATE TRIGGER trg_agency_chat_messages_status_update BEFORE UPDATE OF status ON agency_chat_messages FOR EACH ROW WHEN NEW.status NOT IN ('pending','thinking','acting','waiting','done','failed','cancelled','degraded') BEGIN SELECT RAISE(ABORT, 'invalid agency_chat_messages.status'); END;

CREATE TRIGGER trg_agency_director_actions_status_insert BEFORE INSERT ON agency_director_actions FOR EACH ROW WHEN NEW.status NOT IN ('proposed','approved','executing','done','failed','rejected') BEGIN SELECT RAISE(ABORT, 'invalid agency_director_actions.status'); END;

CREATE TRIGGER trg_agency_director_actions_status_update BEFORE UPDATE OF status ON agency_director_actions FOR EACH ROW WHEN NEW.status NOT IN ('proposed','approved','executing','done','failed','rejected') BEGIN SELECT RAISE(ABORT, 'invalid agency_director_actions.status'); END;

CREATE TRIGGER trg_agency_runs_status_insert BEFORE INSERT ON agency_runs FOR EACH ROW WHEN NEW.status NOT IN ('pending','running','completed','failed','cancelled','idle','observing') BEGIN SELECT RAISE(ABORT, 'invalid agency_runs.status'); END;

CREATE TRIGGER trg_agency_runs_status_update BEFORE UPDATE OF status ON agency_runs FOR EACH ROW WHEN NEW.status NOT IN ('pending','running','completed','failed','cancelled','idle','observing') BEGIN SELECT RAISE(ABORT, 'invalid agency_runs.status'); END;

CREATE TRIGGER trg_editor_gate_records_outcome_insert BEFORE INSERT ON editor_gate_records FOR EACH ROW WHEN NEW.outcome NOT IN ('pass','revise','failed') BEGIN SELECT RAISE(ABORT, 'invalid editor_gate_records.outcome'); END;

CREATE TRIGGER trg_editor_gate_records_outcome_update BEFORE UPDATE OF outcome ON editor_gate_records FOR EACH ROW WHEN NEW.outcome NOT IN ('pass','revise','failed') BEGIN SELECT RAISE(ABORT, 'invalid editor_gate_records.outcome'); END;

CREATE TRIGGER trg_tasks_status_insert BEFORE INSERT ON tasks FOR EACH ROW WHEN NEW.status NOT IN ('pending','running','completed','failed','cancelled') BEGIN SELECT RAISE(ABORT, 'invalid tasks.status'); END;

CREATE TRIGGER trg_tasks_status_update BEFORE UPDATE OF status ON tasks FOR EACH ROW WHEN NEW.status NOT IN ('pending','running','completed','failed','cancelled') BEGIN SELECT RAISE(ABORT, 'invalid tasks.status'); END;

CREATE VIEW v_characters AS
SELECT
    id,
    story_id,
    name,
    json_extract(attributes, '$.background') AS background,
    json_extract(attributes, '$.personality') AS personality,
    json_extract(attributes, '$.goals') AS goals,
    json_extract(attributes, '$.appearance') AS appearance,
    json_extract(attributes, '$.gender') AS gender,
    json_extract(attributes, '$.age') AS age,
    json_extract(attributes, '$.dynamic_traits') AS dynamic_traits,
    source,
    is_auto_generated,
    first_seen AS created_at,
    last_updated AS updated_at,
    json_extract(attributes, '$.emotional_core') AS emotional_core,
    json_extract(attributes, '$.emotional_trigger') AS emotional_trigger,
    json_extract(attributes, '$.emotional_wound') AS emotional_wound,
    json_extract(attributes, '$.emotional_need') AS emotional_need
FROM kg_entities
WHERE entity_type = 'Character' AND is_archived = 0;

CREATE VIEW v_narrative_threads AS
             SELECT
                 id,
                 story_id,
                 'foreshadow' AS thread_type,
                 content AS thread_data,
                 setup_event_id AS target_id,
                 status,
                 importance,
                 created_at
             FROM foreshadowing_tracker;
