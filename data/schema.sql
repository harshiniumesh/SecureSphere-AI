-- ==============================================================================
-- SecureSphere AI - SQLite Database Schema
-- ==============================================================================

-- Enable Foreign Key support in SQLite (Required for cascading deletes)
PRAGMA foreign_keys = ON;

-- ==============================================================================
-- 1. SCENARIOS TABLE
-- Stores the predefined templates available in the Scenario Library.
-- ==============================================================================
CREATE TABLE IF NOT EXISTS scenarios (
    scenario_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    industry TEXT NOT NULL,
    default_revenue REAL NOT NULL CHECK (default_revenue >= 0),
    default_size INTEGER NOT NULL CHECK (default_size > 0),
    critical_asset TEXT NOT NULL
);

-- ==============================================================================
-- 2. SIMULATIONS TABLE
-- Records the user inputs, selected persona, and security configuration for a run.
-- ==============================================================================
CREATE TABLE IF NOT EXISTS simulations (
    sim_id TEXT PRIMARY KEY,
    scenario_id TEXT, -- Nullable if the user creates a custom scenario from scratch
    persona TEXT NOT NULL,
    attack_type TEXT NOT NULL,
    company_name TEXT NOT NULL,
    industry TEXT NOT NULL,
    annual_revenue REAL NOT NULL CHECK (annual_revenue >= 0),
    employee_count INTEGER NOT NULL CHECK (employee_count > 0),
    critical_asset TEXT NOT NULL,

    -- Security Controls (Stored as Integers: 0 for False, 1 for True)
    mfa_enabled INTEGER NOT NULL DEFAULT 0 CHECK (mfa_enabled IN (0, 1)),
    firewall_active INTEGER NOT NULL DEFAULT 0 CHECK (firewall_active IN (0, 1)),
    edr_deployed INTEGER NOT NULL DEFAULT 0 CHECK (edr_deployed IN (0, 1)),
    immutable_backups INTEGER NOT NULL DEFAULT 0 CHECK (immutable_backups IN (0, 1)),
    automated_patching INTEGER NOT NULL DEFAULT 0 CHECK (automated_patching IN (0, 1)),
    employee_training INTEGER NOT NULL DEFAULT 0 CHECK (employee_training IN (0, 1)),

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id) ON DELETE SET NULL
);

-- ==============================================================================
-- 3. SIMULATION_RESULTS TABLE
-- Stores the computed outputs, metrics, and generated timeline for a specific simulation.
-- ==============================================================================
CREATE TABLE IF NOT EXISTS simulation_results (
    result_id TEXT PRIMARY KEY,
    sim_id TEXT NOT NULL,
    risk_score INTEGER NOT NULL CHECK (risk_score >= 0 AND risk_score <= 100),
    readiness_stars INTEGER NOT NULL CHECK (readiness_stars >= 1 AND readiness_stars <= 5),
    financial_loss_min REAL NOT NULL CHECK (financial_loss_min >= 0),
    financial_loss_max REAL NOT NULL CHECK (financial_loss_max >= financial_loss_min),
    timeline_json TEXT NOT NULL, -- Serialized JSON array of the Attack Story Timeline events
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (sim_id) REFERENCES simulations(sim_id) ON DELETE CASCADE
);

-- ==============================================================================
-- 4. LEARNING_TOPICS TABLE
-- Stores the educational content for the Learning Center page.
-- ==============================================================================
CREATE TABLE IF NOT EXISTS learning_topics (
    topic_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    importance TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);