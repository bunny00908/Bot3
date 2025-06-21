import telebot
import json
import time
import re
import threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from p import check_card

BOT_TOKEN = '7390503914:AAFNopMlX6iNHO2HTWNYpLLzE_DfF8h4uQ4'
ADMIN_ID = 5248903529
bot = telebot.TeleBot(BOT_TOKEN)

def load_auth():
    try:
        with open("authorized.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_auth(data):
    with open("authorized.json", "w") as f:
        json.dump(data, f)

AUTHORIZED_USERS = load_auth()

def is_authorized(chat_id):
    if chat_id == ADMIN_ID:
        return True
    if str(chat_id) in AUTHORIZED_USERS:
        expiry = AUTHORIZED_USERS[str(chat_id)]
        if expiry == "forever":
            return True
        if isinstance(expiry, (int, float)) and time.time() < expiry:
            return True
        else:
            del AUTHORIZED_USERS[str(chat_id)]
            save_auth(AUTHORIZED_USERS)
    return False

def normalize_card(text):
    if not text:
        return None
    text = text.replace('\n', ' ').replace('/', ' ')
    numbers = re.findall(r'\d+', text)
    cc = mm = yy = cvv = ''
    for part in numbers:
        if len(part) == 16: cc = part
        elif len(part) == 4 and part.startswith('20'): yy = part
        elif len(part) == 2 and int(part) <= 12 and mm == '': mm = part
        elif len(part) == 2 and not part.startswith('20') and yy == '': yy = '20' + part
        elif len(part) in [3, 4] and cvv == '': cvv = part
    if cc and mm and yy and cvv:
        return f"{cc}|{mm}|{yy}|{cvv}"
    return None

@bot.message_handler(commands=['start'])
def start_handler(msg):
    user_id = msg.from_user.id
    user_name = msg.from_user.first_name or "User"
    username = msg.from_user.username
    display = username if username else user_name

    is_registered = is_authorized(user_id)

    text = (
        "<b>[⌬] Bunny | Version - 1</b>\n"
        "━━━━━━━━━━━━━\n"
        f"Hello, <b>{display}</b>\n"
        "How Can I Help You Today.?! 📊\n"
        f"👤 <b>Your UserID</b> - <code>{user_id}</code>\n"
        "🤖 <b>BOT Status</b> - <b>Online 🟢</b>\n"
    )

    kb = InlineKeyboardMarkup(row_width=2)
    if not is_registered:
        kb.add(
            InlineKeyboardButton("Register", callback_data="register"),
            InlineKeyboardButton("Command", callback_data="command"),
        )
    else:
        kb.add(
            InlineKeyboardButton("Command", callback_data="command"),
        )
    kb.add(InlineKeyboardButton("Close", callback_data="close"))

    bot.send_message(
        msg.chat.id,
        text,
        parse_mode="HTML",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data == "register")
def handle_register(call):
    user_id = call.from_user.id
    AUTHORIZED_USERS[str(user_id)] = "forever"
    save_auth(AUTHORIZED_USERS)
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("Command", callback_data="command"))
    kb.add(InlineKeyboardButton("Close", callback_data="close"))
    bot.edit_message_text(
        f"✅ <b>Registration Complete!</b>\nYou are now registered, <b>{call.from_user.first_name}</b>.",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data == "command")
def command_menu_handler(call):
    text = (
        "<b>JOIN BEFORE USING. ✅</b>\n"
        "- Main : <a href='https://t.me/approvedccm'>Join Now</a>\n"
        "- Chat Group : <a href='https://t.me/approvedccm'>Join Now</a>\n"
        "- Scrapper : <a href='https://t.me/+jLj5grD0l_Y5ZmU1'>Join Now</a>\n"
        "\nChoose Your Gate Type :"
    )
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("Gate", callback_data="gate"),
        InlineKeyboardButton("Tools", callback_data="tools"),
        InlineKeyboardButton("Terms", callback_data="terms")
    )
    kb.add(InlineKeyboardButton("Close", callback_data="close"))
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data == "gate")
def handle_gate_menu(call):
    text = (
        "Bunny [AUTH GATES]\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "【✦】Name: Braintree Auth\n"
        "【✦】Command: <code>/b3 cc|mm|yy|cvv</code>\n"
        "【✦】Status: <b>Active ✅</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "【✦】Name: Stripe Auth\n"
        "【✦】Command: <i>Coming Soon</i>\n"
        "【✦】Status: <b>Coming Soon 🚧</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "【✦】Name: Shopify $1 Auth\n"
        "【✦】Command: <i>Coming Soon</i>\n"
        "【✦】Status: <b>Coming Soon 🚧</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Back", callback_data="command"))
    bot.edit_message_text(
        text, call.message.chat.id, call.message.message_id,
        parse_mode="HTML", reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data == "tools")
def handle_tools_menu(call):
    text = (
        "Bunny [TOOLS]\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "【✦】Name: Bin Info\n"
        "【✦】Command: <code>/bin bin/cc</code>\n"
        "【✦】Status: <b>Coming Soon 🚧</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "【✦】Name: Scrapper\n"
        "【✦】Command: <code>/scr channel 100</code>\n"
        "【✦】Status: <b>Coming Soon 🚧</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "【✦】Name: Fake Random Details\n"
        "【✦】Command: <code>/fake</code>\n"
        "【✦】Status: <b>Coming Soon 🚧</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Back", callback_data="command"))
    bot.edit_message_text(
        text, call.message.chat.id, call.message.message_id,
        parse_mode="HTML", reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data == "terms")
def handle_terms_menu(call):
    text = (
        "Bunny [TERMS]\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Your terms and conditions go here.\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Back", callback_data="command"))
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="HTML",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data == "close")
def close_menu(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass

@bot.message_handler(commands=['auth'])
def authorize_user(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        parts = msg.text.split()
        if len(parts) < 2:
            return bot.reply_to(msg, "❌ Usage: /auth <user_id> [days]")
        user = parts[1]
        days = int(parts[2]) if len(parts) > 2 else None
        if user.startswith('@'):
            return bot.reply_to(msg, "❌ Use numeric Telegram ID, not @username.")
        uid = int(user)
        expiry = "forever" if not days else time.time() + (days * 86400)
        AUTHORIZED_USERS[str(uid)] = expiry
        save_auth(AUTHORIZED_USERS)
        msg_text = f"✅ Authorized {uid} for {days} days." if days else f"✅ Authorized {uid} forever."
        bot.reply_to(msg, msg_text)
    except Exception as e:
        bot.reply_to(msg, f"❌ Error: {e}")

@bot.message_handler(commands=['rm'])
def remove_auth(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        parts = msg.text.split()
        if len(parts) < 2:
            return bot.reply_to(msg, "❌ Usage: /rm <user_id>")
        uid = int(parts[1])
        if str(uid) in AUTHORIZED_USERS:
            del AUTHORIZED_USERS[str(uid)]
            save_auth(AUTHORIZED_USERS)
            bot.reply_to(msg, f"✅ Removed {uid} from authorized users.")
        else:
            bot.reply_to(msg, "❌ User is not authorized.")
    except Exception as e:
        bot.reply_to(msg, f"❌ Error: {e}")

@bot.message_handler(commands=['b3'])
def b3_handler(msg):
    if not is_authorized(msg.from_user.id):
        msg_text = (
            "✖️ <b>Bunny Security Check</b> ✖️\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Oops! You are <u>not allowed</u> to use this bot. 🙁\n"
            "🔐 <b>Reason:</b> <i>Not registered</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📝 <b>Please register by tapping the button below!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Register", callback_data="register"))
        bot.send_message(msg.chat.id, msg_text, parse_mode="HTML", reply_markup=kb)
        return
    args = msg.text.split(None, 1)
    if len(args) < 2:
        error_msg = (
            "🚫 <b>Card Format Error</b> 🚫\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "⟡ Could not extract valid card info from your message.\n"
            "⟡ Please use the correct format to check cards.\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📝 <b>Correct Format Example:</b>\n"
            "<code>/b3 4556737586899855|12|2026|123</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "💡 <b>Tip:</b> You can reply to any message containing a card with <b>/b3</b>.\n"
            "❓ <b>Need help?</b> <a href='https://t.me/Mod_By_Kamal'>Contact Admin</a>\n"
        )
        bot.reply_to(msg, error_msg, parse_mode="HTML")
        return
    cc_line = args[1].strip()
    reply = bot.reply_to(msg, "🔄 <b>Processing...</b>", parse_mode="HTML")
    def run_check():
        try:
            result = check_card(cc_line)
            bot.edit_message_text(result, msg.chat.id, reply.message_id, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            bot.edit_message_text(f"❌ Error: {str(e)}", msg.chat.id, reply.message_id)
    threading.Thread(target=run_check).start()

@bot.message_handler(commands=['mb3'])
def mb3_handler(msg):
    if not is_authorized(msg.from_user.id):
        msg_text = (
            "✖️ <b>Bunny Security Check</b> ✖️\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Oops! You are <u>not allowed</u> to use this bot. 🙁\n"
            "🔐 <b>Reason:</b> <i>Not registered</i>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📝 <b>Please register by tapping the button below!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Register", callback_data="register"))
        bot.send_message(msg.chat.id, msg_text, parse_mode="HTML", reply_markup=kb)
        return
    cards_text = ""
    if msg.reply_to_message:
        cards_text = msg.reply_to_message.text or ""
    else:
        args = msg.text.split(None, 1)
        if len(args) < 2:
            bot.reply_to(msg, "Please send the cards in the message or reply to a card list with /mb3.")
            return
        cards_text = args[1]
    cards_list = [c.strip() for c in cards_text.split('\n') if c.strip()]
    if not cards_list:
        bot.reply_to(msg, "No cards found!")
        return

    approved = 0
    declined = 0
    checked = 0
    total = len(cards_list)

    def get_status_panel():
        return (
            "<b>━━━━━━━━ MASS CHECK STARTED ━━━━━━━━</b>\n"
            "◇ PROCESSING YOUR CARDS...\n"
            "◇ PLEASE WAIT A FEW MOMENTS\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "<b>LIVE STATUS WILL BE UPDATED BELOW</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>APPROVED</b> <b>{approved}</b> 🔥\n"
            f"<b>DECLINED</b> <b>{declined}</b> ❌\n"
            f"<b>TOTAL CHECKED</b> <b>{checked}</b>\n"
            f"<b>TOTAL</b> <b>{total}</b> ✅"
        )

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Close", callback_data="close"))

    status_msg = bot.reply_to(msg, get_status_panel(), parse_mode="HTML", reply_markup=kb)

    def mass_check():
        nonlocal approved, declined, checked
        for card in cards_list:
            try:
                result = check_card(card)
                if "APPROVED" in result:
                    approved += 1
                    bot.send_message(msg.chat.id, result, parse_mode="HTML", disable_web_page_preview=True)
                else:
                    declined += 1
                checked += 1
                try:
                    bot.edit_message_text(
                        get_status_panel(),
                        status_msg.chat.id,
                        status_msg.message_id,
                        parse_mode="HTML",
                        reply_markup=kb
                    )
                except Exception:
                    pass
            except Exception as e:
                declined += 1
                checked += 1
        final_ui = (
            "✅ <b>Mass Checking Complete!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>APPROVED</b> {approved} 🔥\n"
            f"<b>DECLINED</b> {declined} ❌\n"
            f"<b>TOTAL CHECKED</b> {checked}\n"
            f"<b>TOTAL</b> {total} ✅\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "✨ All cards have been processed.\n"
            "🙏 Thank you for using Mass Check!\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )
        try:
            bot.edit_message_text(
                final_ui,
                status_msg.chat.id,
                status_msg.message_id,
                parse_mode="HTML",
                reply_markup=kb
            )
        except Exception:
            pass

    threading.Thread(target=mass_check).start()

if __name__ == "__main__":
    bot.infinity_polling()
