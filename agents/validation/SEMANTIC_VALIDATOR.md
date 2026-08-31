# Validador Semantico Documental

Versao: `0.1.0-draft.8`.

Este validador e evidencia documental reproduzivel. Ele nao e componente de
runtime e nao ativa agentes. O executor le o manifesto de regras, os casos e o
catalogo de gates do R2D2; divergencia de versao, IDs, cobertura ou failure state
falha antes da suite.

Execute a partir da raiz do repositorio:

```ruby
require "yaml"
require "time"
require "json"
require "digest"

load_yaml = lambda do |path|
  YAML.safe_load(File.read(path), permitted_classes: [Time], aliases: false)
end

rules_manifest = load_yaml.call("agents/validation/r2d2-semantic-rules.yaml")
suite = load_yaml.call("agents/validation/semantic-cases.yaml")
r2d2_manifest = load_yaml.call("agents/r2d2/manifest.yaml")
trust_policy = load_yaml.call("agents/validation/trusted-verifiers.yaml")
runner_policy = load_yaml.call("agents/validation/c3po-runner-policy.yaml")

minimum_prohibitions = %w[
  destructive_payloads
  uncontrolled_denial_of_service
  real_data_exfiltration
  unauthorized_persistence
  target_expansion
]

canonical_gate_ids = r2d2_manifest.fetch("gates").map { |gate| gate.fetch("id") }
canonical_gate_owners = r2d2_manifest.fetch("gates").to_h { |gate| [gate.fetch("id"), gate.fetch("owner")] }
canonical_gate_facts = r2d2_manifest.fetch("gates").to_h { |gate| [gate.fetch("id"), gate.fetch("fact")] }
canonical_context_fact_keys = (canonical_gate_facts.values + ["canonical_integration_completed"]).uniq.sort
canonical_gate_version = [
  r2d2_manifest.dig("identity", "canonical_id"),
  r2d2_manifest.dig("identity", "version")
].join("@")

canonicalize = lambda do |value|
  case value
  when Hash
    value.keys.sort.to_h { |key| [key.unicode_normalize(:nfc), canonicalize.call(value.fetch(key))] }
  when Array
    value.map { |item| canonicalize.call(item) }
  when String
    value.unicode_normalize(:nfc).gsub("\r\n", "\n").gsub("\r", "\n")
  when Time
    value.utc.strftime("%Y-%m-%dT%H:%M:%SZ")
  else
    value
  end
end

digest_payload = lambda do |value|
  Digest::SHA256.hexdigest(JSON.generate(canonicalize.call(value)))
end

trust_policy_digest = digest_payload.call(trust_policy)
runner_policy_payload = runner_policy.slice("policy_id", "runners")
runner_policy_digest = digest_payload.call(runner_policy_payload)

valid_prior_record = lambda do |record, expected_type|
  required = %w[record_schema record_type record_id revision state artifact_ref artifact_digest_sha256]
  allowed_states = expected_type == "red_team_engagement" ?
    %w[DRAFT AUTHORIZED ACTIVE CLOSED REVOKED] :
    %w[DRAFT AUTHORIZED ACTIVE CONTAINED RECOVERED CLOSED REVOKED]
  record.is_a?(Hash) && record.keys.sort == required.sort &&
    record.fetch("record_schema") == "r2d2-state-transition-record-v1" &&
    record.fetch("record_type") == expected_type &&
    record.fetch("record_id").is_a?(String) && !record.fetch("record_id").empty? &&
    record.fetch("revision").is_a?(Integer) && record.fetch("revision") >= 1 &&
    allowed_states.include?(record.fetch("state")) &&
    record.fetch("artifact_ref").match?(%r{\Agit-sha256://[0-9a-f]{40}/[A-Za-z0-9._/-]+\.json\z}) &&
    record.fetch("artifact_digest_sha256").match?(/\A[0-9a-f]{64}\z/)
end

resolve_scope_fixture = lambda do |input|
  scope = Marshal.load(Marshal.dump(suite.fetch("validation_scope_fixtures").fetch(input.fetch("validation_scope_ref"))))
  input.fetch("validation_scope_overrides", {}).each do |path, value|
    keys = path.split(".")
    leaf = keys.pop
    target = keys.reduce(scope) { |memo, key| memo.fetch(key) }
    target[leaf] = value
  end
  scope
end

resolve_case_input = lambda do |test_case|
  if test_case.key?("input_fixture_ref")
    input = Marshal.load(Marshal.dump(suite.fetch("input_fixtures").fetch(test_case.fetch("input_fixture_ref"))))
    test_case.fetch("input_overrides", {}).each do |path, value|
      keys = path.split(".")
      leaf = keys.pop
      target = keys.reduce(input) { |memo, key| memo.fetch(key) }
      target[leaf] = value
    end
    test_case.fetch("input_remove", []).each { |key| input.delete(key) }
    input
  else
    test_case.fetch("input")
  end
end

gate_catalog_payload = {
  "identity" => {
    "canonical_id" => r2d2_manifest.dig("identity", "canonical_id"),
    "version" => r2d2_manifest.dig("identity", "version")
  },
  "gates" => r2d2_manifest.fetch("gates").map do |gate|
    gate.slice("id", "when", "fact", "owner", "evidence", "pass_condition")
  end.sort_by { |gate| gate.fetch("id") }
}
canonical_gate_digest = Digest::SHA256.hexdigest(JSON.generate(canonicalize.call(gate_catalog_payload)))

inside_root = lambda do |path, root|
  path == root || path.start_with?(root.end_with?("/") ? root : "#{root}/")
end

partition_exact = lambda do |universe, groups|
  flattened = groups.flatten
  flattened.uniq.length == flattened.length && flattened.sort == universe.sort
end

red_transitions = {
  nil => %w[DRAFT],
  "DRAFT" => %w[AUTHORIZED],
  "AUTHORIZED" => %w[ACTIVE REVOKED],
  "ACTIVE" => %w[CLOSED REVOKED],
  "CLOSED" => [],
  "REVOKED" => []
}

incident_transitions = {
  nil => %w[DRAFT],
  "DRAFT" => %w[AUTHORIZED],
  "AUTHORIZED" => %w[ACTIVE REVOKED],
  "ACTIVE" => %w[CONTAINED REVOKED],
  "CONTAINED" => %w[RECOVERED REVOKED],
  "RECOVERED" => %w[CLOSED REVOKED],
  "CLOSED" => [],
  "REVOKED" => []
}

evaluators = {
  "RED_IDENTITY_SEPARATION" => lambda do |input|
    required = input.values_at("approver", "executor", "kill_switch_operator")
    identities = required + [input["reviewer"]].compact
    required.none? { |value| value.nil? || value.empty? } && input.fetch("approver") == "roberto" &&
      identities.uniq.length == identities.length
  end,
  "RED_TIME_AND_REVOCATION" => lambda do |input|
    approved = Time.parse(input.fetch("approved_at").to_s)
    current = Time.parse(input.fetch("current_at").to_s)
    expires = Time.parse(input.fetch("expires_at").to_s)
    approved < current && current < expires && input.fetch("revoked") == false
  end,
  "RED_KILL_SWITCH_INDEPENDENCE" => lambda do |input|
    tested = Time.parse(input.fetch("tested_at").to_s)
    current = Time.parse(input.fetch("current_at").to_s)
    valid_until = Time.parse(input.fetch("test_valid_until").to_s)
    input.fetch("executor") != input.fetch("operator") && tested <= current && current < valid_until &&
      input.fetch("test_result") == "PASS" && input.fetch("automatic_stop_on_control_loss") == true
  end,
  "RED_SCOPE_DIGEST" => lambda do |input|
    input.fetch("canonicalization_version") == "r2d2-c14n-v1" &&
      input.fetch("recorded") == input.fetch("recalculated")
  end,
  "RED_MINIMUM_PROHIBITIONS" => lambda do |input|
    prohibited = input.fetch("prohibited")
    prohibited.is_a?(Array) && (minimum_prohibitions - prohibited).empty?
  end,
  "RED_RESIDUAL_RISK_OWNER" => lambda do |input|
    input.fetch("residual_risk_owner") == "roberto"
  end,
  "RED_STATE_TRANSITION" => lambda do |input|
    from = input.fetch("from")
    current_record_id = input.fetch("current_record_id")
    current_revision = input.fetch("current_revision")
    previous_ref = input.fetch("previous_record_ref")
    recorded_digest = input.fetch("previous_recorded_digest")
    previous_ok = if from.nil?
      previous_ref.nil? && recorded_digest.nil? && !input.key?("previous_record") &&
        current_record_id.is_a?(String) && !current_record_id.empty? && current_revision == 1
    else
      previous = suite.fetch("previous_record_fixtures").fetch(previous_ref)
      !input.key?("previous_record") && valid_prior_record.call(previous, "red_team_engagement") &&
        previous.fetch("record_id") == current_record_id && previous.fetch("revision") + 1 == current_revision &&
        previous.fetch("state") == from && recorded_digest == digest_payload.call(previous)
    end
    previous_ok && red_transitions.fetch(from).include?(input.fetch("to")) &&
      input.fetch("to") == input.fetch("record_state")
  end,
  "IR_DOUBLE_AUTHORIZATION" => lambda do |input|
    identities_ok = input.fetch("executor") != input.fetch("roberto_identity") &&
      input.fetch("executor") != input.fetch("tereza_identity")
    approvals_ok = input.fetch("roberto_approved") == true && input.fetch("tereza_approved") == true
    digests = input.values_at("recorded_digest", "roberto_digest", "tereza_digest", "recalculated_digest")
    authorities_ok = input.fetch("roberto_identity") == "roberto" && input.fetch("tereza_identity") == "tereza"
    approvals_ok && identities_ok && authorities_ok && input.fetch("canonicalization_version") == "r2d2-c14n-v1" &&
      digests.none?(&:nil?) && digests.uniq.length == 1
  end,
  "IR_TIME_AND_REVOCATION" => lambda do |input|
    current = Time.parse(input.fetch("current_at").to_s)
    roberto_ok = Time.parse(input.fetch("roberto_approved_at").to_s) < current &&
      current < Time.parse(input.fetch("roberto_expires_at").to_s) && input.fetch("roberto_revoked") == false
    tereza_ok = Time.parse(input.fetch("tereza_approved_at").to_s) < current &&
      current < Time.parse(input.fetch("tereza_expires_at").to_s) && input.fetch("tereza_revoked") == false
    roberto_ok && tereza_ok
  end,
  "IR_KILL_SWITCH_INDEPENDENCE" => lambda do |input|
    tested = Time.parse(input.fetch("tested_at").to_s)
    current = Time.parse(input.fetch("current_at").to_s)
    valid_until = Time.parse(input.fetch("test_valid_until").to_s)
    input.fetch("executor") != input.fetch("operator") && tested <= current && current < valid_until &&
      input.fetch("test_result") == "PASS" && input.fetch("automatic_stop_on_control_loss") == true
  end,
  "IR_STATE_TRANSITION" => lambda do |input|
    from = input.fetch("from")
    current_record_id = input.fetch("current_record_id")
    current_revision = input.fetch("current_revision")
    previous_ref = input.fetch("previous_record_ref")
    recorded_digest = input.fetch("previous_recorded_digest")
    previous_ok = if from.nil?
      previous_ref.nil? && recorded_digest.nil? && !input.key?("previous_record") &&
        current_record_id.is_a?(String) && !current_record_id.empty? && current_revision == 1
    else
      previous = suite.fetch("previous_record_fixtures").fetch(previous_ref)
      !input.key?("previous_record") && valid_prior_record.call(previous, "incident_response") &&
        previous.fetch("record_id") == current_record_id && previous.fetch("revision") + 1 == current_revision &&
        previous.fetch("state") == from && recorded_digest == digest_payload.call(previous)
    end
    previous_ok && incident_transitions.fetch(from).include?(input.fetch("to")) &&
      input.fetch("to") == input.fetch("record_state")
  end,
  "HANDOFF_GATE_COMPLETENESS" => lambda do |input|
    gate_ids = input.fetch("gate_ids")
    applicable = input.fetch("applicable_ids")
    not_applicable = input.fetch("not_applicable_ids")
    pass_ids = input.fetch("pass_ids")
    pending = input.fetch("pending_ids")
    blocked = input.fetch("blocked_ids")
    evidence = input.fetch("evidence_ids")
    arrays = [gate_ids, applicable, not_applicable, pass_ids, pending, blocked, evidence]
    next false unless arrays.all? { |value| value.is_a?(Array) }
    next false unless gate_ids.uniq.length == gate_ids.length && gate_ids.sort == canonical_gate_ids.sort
    context = suite.fetch("context_fixtures").fetch(input.fetch("canonical_task_context_ref"))
    binding = input.fetch("task_context_binding")
    verification = suite.fetch("verification_receipt_fixtures").fetch(binding.fetch("verification_receipt_ref"))
    source_bundle = suite.fetch("source_bundle_fixtures").fetch(context.fetch("source_bundle_ref"))
    attestation = suite.fetch("identity_attestation_fixtures").fetch(verification.fetch("authentication_evidence_ref"))
    owners = input.fetch("gate_owners")
    next false unless [context, binding, verification, source_bundle, attestation, owners].all? { |value| value.is_a?(Hash) }
    facts = context.fetch("facts")
    source_facts = source_bundle.fetch("facts")
    context_keys = %w[schema_version context_schema context_id repository producer_identity source_bundle_ref source_bundle_digest_sha256 extractor_id extractor_digest_sha256 facts]
    source_keys = %w[source_schema repository facts]
    repository_keys = %w[repository_id base_sha head_sha source_root_realpath exact_pathset_digest_sha256]
    receipt_keys = %w[receipt_schema verification_id context_id context_ref verified_context_digest_sha256 source_bundle_ref verified_source_bundle_digest_sha256 extractor_id extractor_digest_sha256 verifier_identity verifier_credential_fingerprint_sha256 trust_policy_id trust_policy_digest_sha256 authentication_evidence_ref authentication_evidence_digest_sha256 verified_at result receipt_digest_sha256]
    attestation_keys = %w[attestation_schema identity credential_fingerprint_sha256 trust_root_ref assertion authenticated]
    next false unless context.keys.sort == context_keys.sort && source_bundle.keys.sort == source_keys.sort &&
      context.fetch("repository").keys.sort == repository_keys.sort &&
      source_bundle.fetch("repository").keys.sort == repository_keys.sort &&
      verification.keys.sort == receipt_keys.sort && attestation.keys.sort == attestation_keys.sort
    next false unless source_bundle.fetch("source_schema") == "r2d2-context-source-v1"
    next false unless facts.is_a?(Hash) && source_facts.is_a?(Hash)
    next false unless facts.keys.sort == canonical_context_fact_keys && source_facts.keys.sort == canonical_context_fact_keys
    next false unless facts.values.all? { |value| [true, false].include?(value) }
    next false unless facts == source_facts
    source_digest = digest_payload.call(source_bundle)
    context_digest = digest_payload.call(context)
    context_repository = context.fetch("repository")
    source_repository = source_bundle.fetch("repository")
    verification_payload = verification.reject { |key, _value| key == "receipt_digest_sha256" }
    verification_digest = digest_payload.call(verification_payload)
    attestation_digest = digest_payload.call(attestation)
    trusted_verifier = trust_policy.fetch("trusted_verifiers").find do |entry|
      entry.fetch("identity") == verification.fetch("verifier_identity") &&
        entry.fetch("credential_fingerprint_sha256") == verification.fetch("verifier_credential_fingerprint_sha256") &&
        entry.fetch("allowed_assertions").include?("task_context")
    end
    context_binding_ok = binding.fetch("context_schema") == "r2d2-task-context-v1" &&
      context.fetch("context_schema") == "r2d2-task-context-v1" &&
      binding.fetch("context_id") == context.fetch("context_id") &&
      binding.fetch("context_ref") == "store://contexts/#{context.fetch("context_id")}.json" &&
      binding.fetch("context_digest_sha256") == context_digest &&
      binding.fetch("producer_identity") == context.fetch("producer_identity") &&
      binding.fetch("verifier_identity") == verification.fetch("verifier_identity") &&
      binding.fetch("verification_id") == verification.fetch("verification_id") &&
      binding.fetch("verification_receipt_ref") == "store://verifications/#{verification.fetch("verification_id")}.json" &&
      binding.fetch("verification_receipt_digest_sha256") == verification.fetch("receipt_digest_sha256") &&
      verification.fetch("receipt_digest_sha256") == verification_digest &&
      verification.fetch("receipt_schema") == "r2d2-context-verification-receipt-v1" &&
      verification.fetch("result") == "PASS" &&
      binding.fetch("verified_at") == verification.fetch("verified_at") &&
      verification.fetch("context_id") == context.fetch("context_id") &&
      verification.fetch("context_ref") == binding.fetch("context_ref") &&
      verification.fetch("verified_context_digest_sha256") == context_digest &&
      verification.fetch("source_bundle_ref") == context.fetch("source_bundle_ref") &&
      verification.fetch("verified_source_bundle_digest_sha256") == source_digest &&
      context.fetch("source_bundle_digest_sha256") == source_digest &&
      verification.fetch("extractor_id") == context.fetch("extractor_id") &&
      verification.fetch("extractor_digest_sha256") == context.fetch("extractor_digest_sha256") &&
      verification.fetch("trust_policy_id") == trust_policy.fetch("policy_id") &&
      verification.fetch("trust_policy_digest_sha256") == trust_policy_digest &&
      verification.fetch("authentication_evidence_digest_sha256") == attestation_digest &&
      attestation.fetch("authenticated") == true &&
      attestation.fetch("identity") == verification.fetch("verifier_identity") &&
      attestation.fetch("credential_fingerprint_sha256") == verification.fetch("verifier_credential_fingerprint_sha256") &&
      attestation.fetch("trust_root_ref") == trust_policy.fetch("trust_root_ref") &&
      attestation.fetch("assertion") == "task_context" &&
      !trusted_verifier.nil? &&
      verification.fetch("verifier_identity") != context.fetch("producer_identity") &&
      verification.fetch("verifier_identity") != input.fetch("handoff_owner") &&
      verification.fetch("receipt_digest_sha256").match?(/\A[0-9a-f]{64}\z/) &&
      Time.parse(verification.fetch("verified_at").to_s) <= Time.parse(input.fetch("handoff_created_at").to_s) &&
      source_repository == context_repository &&
      context_repository.fetch("repository_id") == input.fetch("handoff_repository") &&
      context_repository.fetch("head_sha") == input.fetch("handoff_head") &&
      context_repository.fetch("source_root_realpath") == input.fetch("handoff_source_root") &&
      context_repository.fetch("exact_pathset_digest_sha256") == input.fetch("handoff_pathset_digest")
    next false unless context_binding_ok
    derived_applicable = canonical_gate_ids.select { |id| facts.fetch(canonical_gate_facts.fetch(id)) }
    state_requires_integration = input.fetch("handoff_state") == "COMMITTED"
    integration_complete = facts.fetch("artifact_submitted_to_canonical_integration") &&
      facts.fetch("canonical_integration_completed") && pass_ids.include?("C3PO_CEPO_INTEGRATED")
    input.fetch("gate_catalog_version") == canonical_gate_version &&
      input.fetch("expected_gate_catalog_version") == canonical_gate_version &&
      input.fetch("recorded_digest") == canonical_gate_digest &&
      input.fetch("recalculated_digest") == canonical_gate_digest &&
      owners == canonical_gate_owners && applicable.sort == derived_applicable.sort &&
      partition_exact.call(gate_ids, [applicable, not_applicable]) &&
      partition_exact.call(applicable, [pass_ids, pending, blocked]) &&
      evidence.uniq.sort == gate_ids.sort && (!state_requires_integration || integration_complete)
  end,
  "HANDOFF_STATE_CONSISTENCY" => lambda do |input|
    artifact_states = input.fetch("artifact_states")
    gate_statuses = input.fetch("gate_statuses")
    relationships = input.fetch("relationships")
    test_statuses = input.fetch("test_statuses")
    arrays = [artifact_states, gate_statuses, relationships, test_statuses]
    raise TypeError unless arrays.all? { |value| value.is_a?(Array) }
    committed = input.fetch("state") == "COMMITTED"
    consistent = !artifact_states.empty? && artifact_states.all? { |state| state == "COMMITTED" } &&
      !gate_statuses.empty? && (gate_statuses & %w[BLOCKED PENDING]).empty? &&
      !relationships.empty? && !relationships.include?("conflito") &&
      test_statuses.include?("PASS") && (test_statuses & %w[FAIL NOT_RUN]).empty?
    !committed || consistent
  end,
  "C3PO_ZERO_MUTATION" => lambda do |input|
    declared_equal = input.fetch("declared_head") == input.fetch("before_head") &&
      input.fetch("declared_head") == input.fetch("after_head") &&
      input.fetch("declared_branch") == input.fetch("before_branch") &&
      input.fetch("declared_branch") == input.fetch("after_branch") &&
      input.fetch("declared_boundary") == input.fetch("before_boundary") &&
      input.fetch("declared_boundary") == input.fetch("after_boundary")
    proofs_equal = %w[worktree status stage refs].all? do |name|
      input.fetch("before_#{name}") == input.fetch("after_#{name}")
    end
    counts_zero = input.fetch("source_mutations") == 0 && input.fetch("git_mutations") == 0 &&
      input.fetch("outside_output_mutations") == 0
    declared_equal && proofs_equal && counts_zero
  end,
  "C3PO_HANDOFF_AUTHORIZATION_BINDING" => lambda do |input|
    scope = resolve_scope_fixture.call(input)
    authorization = input.fetch("authorization")
    binding = scope.fetch("handoff_binding")
    handoff = suite.fetch("handoff_fixtures").fetch(binding.fetch("handoff_ref"))
    approved = Time.parse(input.fetch("approved_at").to_s)
    current = Time.parse(input.fetch("current_at").to_s)
    expires = Time.parse(input.fetch("expires_at").to_s)
    handoff_digests = input.values_at("handoff_recorded_digest", "handoff_recalculated_digest")
    handoff_digest = digest_payload.call(handoff)
    scope_digest = digest_payload.call(scope)
    handoff_repository = handoff.fetch("repository")
    handoff_paths = handoff.fetch("exact_pathset")
    handoff_keys = %w[schema_version handoff_id created_at source_agent target_agent state owner_id objective repository exact_pathset artifacts dependencies task_context_binding gate_catalog_version gate_catalog_digest_sha256 gates relationships version_impact tests rollback next_action]
    handoff_shape_ok = handoff.keys.sort == handoff_keys.sort && handoff.fetch("schema_version") == 1 &&
      handoff.fetch("source_agent") == "r2d2-global" && handoff.fetch("target_agent") == "c3po-cepo" &&
      handoff.fetch("artifacts").is_a?(Array) && !handoff.fetch("artifacts").empty? &&
      handoff.fetch("gates").is_a?(Array) && handoff.fetch("gates").length == canonical_gate_ids.length &&
      handoff.fetch("gates").map { |gate| gate.fetch("id") }.sort == canonical_gate_ids.sort &&
      handoff.fetch("relationships").is_a?(Array) && !handoff.fetch("relationships").empty? &&
      handoff.fetch("tests").is_a?(Array) && !handoff.fetch("tests").empty?
    identity_match = authorization.fetch("owner_identity") == input.fetch("handoff_owner") &&
      binding.fetch("source_owner_id") == handoff.fetch("owner_id") &&
      handoff.fetch("owner_id") == input.fetch("handoff_owner") &&
      binding.fetch("target_agent") == "c3po-cepo"
    handoff_id_match = binding.fetch("handoff_id") == handoff.fetch("handoff_id") &&
      handoff.fetch("handoff_id") == input.fetch("source_handoff_id")
    repository_match = binding.fetch("repository_id") == handoff_repository.fetch("repository_id") &&
      binding.fetch("head_sha") == handoff_repository.fetch("head_sha") &&
      binding.fetch("branch") == handoff_repository.fetch("branch") &&
      binding.fetch("worktree_id") == handoff_repository.fetch("worktree_id") &&
      binding.fetch("source_root_realpath") == handoff_repository.fetch("source_root_realpath") &&
      handoff_repository.fetch("repository_id") == input.fetch("handoff_repository") &&
      handoff_repository.fetch("head_sha") == input.fetch("handoff_head") &&
      handoff_repository.fetch("branch") == input.fetch("handoff_branch") &&
      handoff_repository.fetch("worktree_id") == input.fetch("handoff_worktree") &&
      handoff_repository.fetch("source_root_realpath") == input.fetch("handoff_source_root") &&
      scope.fetch("repository_id") == input.fetch("handoff_repository") &&
      scope.fetch("head_sha") == input.fetch("handoff_head") &&
      scope.fetch("branch") == input.fetch("handoff_branch") &&
      scope.fetch("worktree_id") == input.fetch("handoff_worktree") &&
      scope.fetch("source_root_realpath") == input.fetch("handoff_source_root")
    validation_paths = scope.fetch("authorized_source_pathset")
    source_root = scope.fetch("source_root_realpath")
    command_path = scope.fetch("command_source_realpath")
    argv = scope.fetch("command_argv")
    argv_index = scope.fetch("command_source_argv_index")
    pathset_digest = digest_payload.call(validation_paths.uniq.sort)
    runner = runner_policy.fetch("runners").fetch(scope.fetch("runner_id"))
    forbidden_shells = runner.fetch("forbidden_executable_basenames")
    forbidden_inline_flags = runner.fetch("forbidden_inline_flags")
    runner_ok = scope.fetch("runner_policy_id") == runner_policy.fetch("policy_id") &&
      scope.fetch("runner_policy_digest_sha256") == runner_policy_digest &&
      scope.fetch("runner_executable_realpath") == runner.fetch("executable_realpath") &&
      scope.fetch("runner_executable_digest_sha256") == runner.fetch("executable_digest_sha256") &&
      scope.fetch("direct_exec_only") == true && scope.fetch("arbitrary_shell") == "DENY" &&
      scope.fetch("inline_code") == "DENY" && runner.fetch("direct_exec_only") == true &&
      runner.fetch("arbitrary_shell") == "DENY" && runner.fetch("inline_code") == "DENY" &&
      argv.is_a?(Array) && !argv.empty? && argv.fetch(0) == runner.fetch("executable_realpath") &&
      !forbidden_shells.include?(File.basename(argv.fetch(0))) &&
      (argv & forbidden_inline_flags).empty? &&
      argv_index.is_a?(Integer) && argv_index >= 0 && argv_index == runner.fetch("required_source_argv_index") &&
      argv_index < argv.length && argv.fetch(argv_index) == command_path
    paths_match = handoff_paths.is_a?(Array) && validation_paths.is_a?(Array) &&
      handoff_paths.sort == validation_paths.sort &&
      input.fetch("handoff_paths").sort == handoff_paths.sort &&
      validation_paths.all? { |path| inside_root.call(path, source_root) } &&
      validation_paths.any? { |path| inside_root.call(command_path, path) } &&
      inside_root.call(command_path, source_root) &&
      inside_root.call(scope.fetch("working_directory"), source_root) &&
      inside_root.call(scope.fetch("git_metadata_realpath"), source_root) &&
      scope.fetch("command_source_path") == command_path.delete_prefix("#{source_root}/")
    digest_binding = binding.fetch("handoff_digest_sha256") == handoff_digest &&
      handoff_digests.all? { |digest| digest == handoff_digest } &&
      binding.fetch("exact_pathset_digest_sha256") == input.fetch("handoff_pathset_digest") &&
      scope.fetch("authorized_source_pathset_digest_sha256") == pathset_digest &&
      binding.fetch("exact_pathset_digest_sha256") == pathset_digest &&
      scope.fetch("command_source_digest_sha256") == input.fetch("command_recalculated_digest") &&
      authorization.fetch("validation_scope_digest_sha256") == scope_digest
    authorization_current = approved < current && current < expires &&
      authorization.fetch("approved_at") == input.fetch("approved_at") &&
      authorization.fetch("expires_at") == input.fetch("expires_at") &&
      authorization.fetch("revoked_at").nil?
    authorization_current && handoff_shape_ok && handoff_id_match && identity_match && repository_match &&
      runner_ok && paths_match && digest_binding && handoff_digests.none?(&:nil?) &&
      scope.fetch("network") == "DENY" && scope.fetch("secrets") == "DENY" &&
      scope.fetch("installation") == "DENY" && scope.fetch("runtime_mutation") == "DENY" &&
      scope.fetch("source_tree_read_only") == true && scope.fetch("git_metadata_read_only") == true
  end,
  "C3PO_PATHSET_ISOLATION" => lambda do |input|
    source = input.fetch("source_root")
    git = input.fetch("git_root")
    working = input.fetch("working_directory")
    output = input.fetch("output_root")
    writable = input.fetch("writable_paths")
    observed = input.fetch("observed_paths")
    paths_are_arrays = writable.is_a?(Array) && observed.is_a?(Array)
    roots_are_absolute = [source, git, working, output].all? { |path| path.is_a?(String) && path.start_with?("/") }
    working_inside_source = inside_root.call(working, source)
    output_disjoint = !inside_root.call(output, source) && !inside_root.call(source, output) &&
      !inside_root.call(output, git) && !inside_root.call(git, output)
    all_inside = paths_are_arrays && (writable + observed).all? { |path| inside_root.call(path, output) }
    roots_are_absolute && working_inside_source && output_disjoint && all_inside && input.fetch("output_root_ephemeral") == true &&
      input.fetch("traversal_segments") == 0 && input.fetch("symlink_escapes") == 0 &&
      input.fetch("unresolved_paths") == 0
  end,
  "C3PO_EXECUTION_RESULT" => lambda do |input|
    started = Time.parse(input.fetch("started_at").to_s)
    finished = Time.parse(input.fetch("finished_at").to_s)
    expected_outputs = input.fetch("expected_outputs")
    observed_outputs = input.fetch("observed_outputs")
    input.fetch("state") == "PASS" && input.fetch("observed_result") == "PASS" &&
      input.fetch("expected_exit_codes").include?(input.fetch("exit_code")) &&
      expected_outputs.is_a?(Array) && observed_outputs.is_a?(Array) &&
      (expected_outputs - observed_outputs).empty? && started <= finished
  end,
  "C3PO_PRECHECK_FAIL_CLOSED" => lambda do |input|
    input.fetch("state") == "BLOCKED" && input.fetch("blocked_phase") == "PRECHECK" &&
      input.fetch("observed_result") == "NOT_RUN" && input.fetch("exit_code").nil? &&
      input.fetch("started_at").nil? && input.fetch("finished_at").nil? &&
      input.fetch("output_artifacts") == [] && input.fetch("before_present") == false &&
      input.fetch("after_present") == false
  end
}

declared_rules = rules_manifest.fetch("rules")
declared_ids = declared_rules.map { |rule| rule.fetch("id") }
abort "DUPLICATE_DECLARED_RULE" unless declared_ids.uniq.length == declared_ids.length
abort "RULE_IMPLEMENTATION_DRIFT" unless declared_ids.sort == evaluators.keys.sort
abort "VERSION_DRIFT" unless rules_manifest.fetch("version") == suite.fetch("version")
abort "RUNTIME_MUST_REMAIN_DISABLED" unless rules_manifest.fetch("runtime_enabled") == false
case_rule_ids = suite.fetch("cases").map { |test_case| test_case.fetch("rule") }
abort "RULE_WITHOUT_CASE" unless (declared_ids - case_rule_ids).empty?
failure_states = declared_rules.to_h { |rule| [rule.fetch("id"), rule.fetch("failure_state")] }

evaluate = lambda do |rule, input|
  evaluator = evaluators[rule]
  next "DENY_UNKNOWN_RULE" unless evaluator
  evaluator.call(input) ? "PASS" : failure_states.fetch(rule)
rescue KeyError, TypeError, ArgumentError, NoMethodError
  "DENY_INVALID_INPUT"
end

failures = []
suite.fetch("cases").each do |test_case|
  actual = evaluate.call(test_case.fetch("rule"), resolve_case_input.call(test_case))
  expected = test_case.fetch("expected")
  puts "#{test_case.fetch("id")}: #{actual}"
  failures << [test_case.fetch("id"), expected, actual] unless actual == expected
end

abort "SEMANTIC_VALIDATION_FAILED #{failures.inspect}" unless failures.empty?
puts "SEMANTIC_VALIDATION_PASS cases=#{suite.fetch("cases").length} rules=#{declared_ids.length}"
```

Qualquer regra desconhecida, campo ausente, tipo invalido ou excecao termina em
negacao. Um futuro consumidor de runtime deve implementar contrato equivalente,
usar o mesmo algoritmo de canonicalizacao e possuir testes independentes antes
de ativacao.
