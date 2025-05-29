import pytest
import os
from datetime import date
from typing import Dict, List, Optional
import sys

# テスト時にモジュールを正しく読み込むために、テスト用の環境変数を設定
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/library_test"
os.environ["TEST_MODE"] = "1"
