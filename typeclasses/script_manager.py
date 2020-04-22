from evennia import create_script, GLOBAL_SCRIPTS, logger, signals
from evennia.server.sessionhandler import SESSION_HANDLER


def attach_signal_handlers():
  try:
    signals.SIGNAL_ACCOUNT_POST_LOGIN.connect(login_handler)
    signals.SIGNAL_ACCOUNT_POST_LOGOUT.connect(logout_handler)
  except Exception as e:
    logger.log_error(e)


def login_handler(sender, **kwargs):
  # make sure global scripts have started
  start_global_scripts()
  #logger.log_info(f"login account_count: {SESSION_HANDLER.account_count()}")
  #logger.log_info(f"{SESSION_HANDLER.all_connected_accounts()}")


def logout_handler(sender, **kwargs):
  # if we're the last one out, turn off the lights
  #logger.log_info(f"login account_count: {SESSION_HANDLER.account_count()}")
  #logger.log_info(f"{SESSION_HANDLER.all_connected_accounts()}")
  if SESSION_HANDLER.account_count() == 0:
    stop_global_scripts()


def start_global_scripts():
  # TODO: use one global state var?
  if not GLOBAL_SCRIPTS.behavior_ticker:
    create_script("typeclasses.scripts.BehaviorTicker", 
      key="behavior_ticker", persistent=False, obj=None)

  if not GLOBAL_SCRIPTS.health_ticker:
    create_script("typeclasses.scripts.HealthTicker", 
      key="health_ticker", persistent=False, obj=None)


def stop_global_scripts():
  GLOBAL_SCRIPTS.behavior_ticker.stop()
  GLOBAL_SCRIPTS.health_ticker.stop()
    



