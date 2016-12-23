using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ServiceModel;
using System.ServiceModel.Channels;
using System.Configuration;

namespace Cosmweb.Net.WCF
{
    /// <summary>
    /// ｻｰﾋﾞｽﾎｽﾄの拡張ｸﾗｽ
    /// </summary>
    public class ServiceHostExtention : ServiceHost
    {
        public object Tag { get; set; }
        public ServiceHostExtention() : base()
        {
        }

        public ServiceHostExtention(Object obj, params Uri[] uri) : base(obj, uri)
        {

        }

        public ServiceHostExtention(Type type, params  Uri[] uri)
            : base(type, uri)
        { }
    }

	public abstract class WcfHostBase<TService>
	{
		/// <summary>
		/// デフォルトアドレス
		/// </summary>
		public const string DEFAULT_HOST_URL = "net.tcp://localhost:8080/Service";

		/// <summary>
		/// サービスホスト
		/// </summary>
        private ServiceHostExtention _host;
        protected ServiceHostExtention Host
		{
			get { return _host; }
		}

		/// <summary>
		/// クライアント→ホスト間で使用する最大メッセージサイズ（適当に大きなサイズを指定）
		/// </summary>
		public readonly long DefaultMaxMessageSize = 400000;

		/// <summary>
		/// コンストラクタ
		/// </summary>
		public WcfHostBase()
		{
		}

		/// <summary>
		/// コンストラクタ
		/// ※　最大メッセージサイズはデフォルト(MSDN参照)
		/// </summary>
		/// <param name="type"></param>
		/// <param name="serviceURL"></param>
		public WcfHostBase(Type type, string serviceURL)
		{
			Create(type, serviceURL, new NetTcpBinding());
		}

		/// <summary>
		/// ホストサービスの作成
		/// </summary>
		public void Create()
		{
            Create(typeof(WcfHostBase<TService>), DEFAULT_HOST_URL, this.DefaultMaxMessageSize);
		}

		/// <summary>
		/// ホストサービスの作成
        /// <param name="type"></param>
        /// <param name="serviceURL"></param>
        /// <param name="maxMessageSize"></param>
		/// </summary>
		public void Create(Type type, string serviceURL, long maxMessageSize)
		{
			Create(type, serviceURL, new NetTcpBinding { MaxReceivedMessageSize = maxMessageSize });
		}

		/// <summary>
		/// ホストサービスの作成
		/// 例外は上位で捉え。
		/// </summary>
		/// <param name="type"></param>
        /// <param name="serviceURL"></param>
        /// <param name="binding"></param>
		public void Create(Type type, string serviceURL, Binding binding)
		{
			try
			{
                _host = new ServiceHostExtention(type);
				_host.AddServiceEndpoint
					(
                    typeof(TService),
					binding,
					serviceURL
					);

				// 各種イベント登録
				_host.Faulted += _host_Faulted;
				_host.Opened += _host_Opened;
				_host.Closed += _host_Closed;
                _host.UnknownMessageReceived += _host_UnknownMessageReceived;
			}
			catch
			{
				throw;
			}
		}

		/// <summary>
		/// 開始
		/// </summary>
        public CommunicationState Start()
		{
			// オープン済み？
			if (_host.State == CommunicationState.Opened )
			{
                return CommunicationState.Opened;
			}
			_host.Open();

            return _host.State;
		}

		/// <summary>
		/// クローズイベント
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		public virtual void _host_Closed(object sender, EventArgs e)
		{
		}

		/// <summary>
		/// オープンイベント
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		public virtual void _host_Opened(Object sender, EventArgs e)
		{
		}

		/// <summary>
		/// 異常イベント
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		public virtual void _host_Faulted(Object sender, EventArgs e)
		{
		}
        
        /// <summary>
        /// 不明電文
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        public virtual void _host_UnknownMessageReceived(object sender, UnknownMessageReceivedEventArgs e)
        {
        }

		/// <summary>
		/// 
		/// </summary>
		public virtual void Close()
		{
            var channel = (_host as IChannel);
            if( channel == null)
            {
                return;
            }

            channel.Close();
		}
	}
}
