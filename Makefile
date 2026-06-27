.PHONY: push test test-full

# 推送（通过 GitHub REST API，避免 git push 网络问题）
push:
	@echo "Pushing via GitHub REST API..."
	@python3 scripts/push_to_github.py "$(m)"

# 运行测试
test:
	cd hermes-component && python3 -m pytest tests/ -q

# 隔离检查
test-full: test
	cd hermes-component && python3 tests/lint/check_import_isolation.py .
