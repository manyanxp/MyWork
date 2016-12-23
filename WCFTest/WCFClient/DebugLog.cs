using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Diagnostics;
using System.Reflection;
using NLog;
using NLog.Config;

namespace WCFClient.Logger
{
	/// <summary>
	///		デバッグログクラス
	/// </summary>
    public static class DebugLog
    {
        private static NLog.Logger _logger = LogManager.GetLogger("logger");

		/// <summary>
		///		一般的情報ログメッセージ出力用
		/// </summary>
		/// <param name="message"></param>
        public static void LogInfo(string message)
        {
            _logger.Info(message);
        }

		/// <summary>
		///		デバッグ情報ログメッセージ出力用
		/// </summary>
		/// <param name="message"></param>
        public static void LogDebug(string message)
        {
            _logger.Debug(AddCallString(message));
        }

		/// <summary>
		///		致命的エラーメッセージ出力用
		/// </summary>
		/// <param name="message"></param>
		public static void LogFatal(string message)
		{
			_logger.Fatal(AddCallString(message));
		}

		/// <summary>
		///		エラーログメッセージ出力用
		/// </summary>
		/// <param name="message"></param>
        public static void LogError(string message)
        {
            _logger.Error(AddCallString(message));
        }

        /// <summary>
        /// 例外詳細出力用
        /// </summary>
        /// <param name="e"></param>
        /// <param name="message"></param>
        public static void LogException(Exception e, string message = "")
        {
            _logger.Error(e, message);
        }
        
		/// <summary>
		///		警告ログメッセージ出力用
		/// </summary>
		/// <param name="message"></param>
		public static void LogWarn(string message)
		{
			_logger.Warn(AddCallString(message));
		}

        /// <summary>
        /// ATSシステム定数ダンプ用
        /// </summary>
        /// <param name="str"></param>
        /// <param name="data"></param>
        public static void LogDebugDump(string str, byte[] data)
        {
            _logger.Info(str + " " + BitConverter.ToString(data));
        }

		/// <summary>
		///		ログテキスト登録
		/// </summary>
		/// <param name="logtext"></param>
		/// <returns></returns>
        private static string AddCallString(string logtext)
        {
            try
            {
                StackFrame callerFrame = new StackFrame(2);
                if(callerFrame != null)
                {
                    MethodBase callerMethod = callerFrame.GetMethod();
                    if(callerMethod != null)
                    {
                        logtext += "\tclass:" + callerMethod.DeclaringType.Name + "\tmethod:" + callerMethod;
                    }
                }

            }
            catch (Exception)
            {
                // 何もしない
            }

            return logtext;
        }
    }
}
