import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from dashboard.app import main
if __name__ == "__main__":
    main()