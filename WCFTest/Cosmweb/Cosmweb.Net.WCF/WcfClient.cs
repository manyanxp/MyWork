using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.ServiceModel;
using System.ServiceModel.Description;
using System.ServiceModel.Channels;
using WcfService;
namespace Cosmweb.Net.WCF
{
	/// <summary>
	/// WCFクライアント
	/// </summary>
	/// <typeparam name="T"></typeparam>
    public abstract class WcfClientBase<THost> : IDisposable
	{
		/// <summary>
		/// デフォルトアドレス
		/// </summary>
		public const string DEFAULT_SERVER_URL = "net.tcp://localhost:8080/Service";
        public InstanceContext CallBack {  get;  set; }
		/// <summary>
		/// サーバーアドレス
		/// </summary>
		string _server_url = "";
		public string ServerUrl
		{
			get { return _server_url; }
			set { _server_url = value; }
		}

		/// <summary>
		/// チャネル
		/// </summary>
        private THost _host;
        public THost Host
		{
            get { return _host; }
		}

		/// <summary>
		/// 接続済み
		/// </summary>
		public bool IsConnected
		{
			get 
			{
                if (_host == null)
				{
					return false;
				}
                return ((_host as IChannel).State == CommunicationState.Opened ? true : false); 
			}
		}

		/// <summary>
		/// 接続状態
		/// </summary>
		public CommunicationState State
		{
			get 
			{
                if (_host == null)
				{
					return CommunicationState.Closed;
				}
                return (_host as IChannel).State;
			}
		}


		/// <summary>
		/// コンストラクタ
		/// </summary>
		public WcfClientBase()
		{
		}

		/// <summary>
		/// チャネル作成
		/// </summary>
		public void CreateChannel()
		{
			_server_url = DEFAULT_SERVER_URL;
			CreateChannel(DEFAULT_SERVER_URL);
		}

		/// <summary>
		/// チャネル作成
		/// </summary>
		/// <param name="server_url">サーバーのURL</param>
		public void CreateChannel(string server_url)
		{
            this._server_url = server_url ?? DEFAULT_SERVER_URL;
            CreateChannel(new NetTcpBinding(), server_url);
		}

		/// <summary>
		/// チャネル作成
		/// </summary>
		/// <param name="binding">Binding</param>
		/// <param name="server_url">サーバーのURL</param>
		public void CreateChannel(Binding binding, string server_url)
		{
            this._server_url = server_url ?? DEFAULT_SERVER_URL;
            CreateChannel(binding, new EndpointAddress(server_url));
		}

		/// <summary>
		/// チャネル作成
		/// </summary>
		/// <param name="binding"></param>
		/// <param name="addresss"></param>
        public void CreateChannel(Binding binding, EndpointAddress addresss)
		{
            if( CallBack == null)
            {
                throw new ArgumentNullException();
            }
            binding.CloseTimeout = new TimeSpan(0, 0, 1);
            
			try
			{
                _host = new DuplexChannelFactory<THost>(
                   CallBack,
                   binding,
				   addresss
				).CreateChannel();
			}
			catch
			{
				throw;
			}
		}

		/// <summary>
		/// Dispose
		/// </summary>
		public void Dispose()
		{
			Dispose(true);
		}

		/// <summary>
		/// Dispose
		/// </summary>
		/// <param name="disposing"></param>
		public void Dispose(bool disposing)
		{
			if (disposing)
			{
				// 何かリソース解放（有れば）
				;
			}

			this.DisposeService();
			GC.SuppressFinalize(this);
		}

		/// <summary>
		/// サーバーと接続
		/// </summary>
		public void Open()
		{
			Exception mostRecentEx = null;
            if (_host != null)
			{
                var service = (_host as IChannel);
				// 接続済み？
				if (service.State == CommunicationState.Opened)
				{
					return;
				}

				// イベント登録
				service.Opened += OnOpened;
				service.Closed += OnClosed;
				service.Closing += OnClosing;
				service.Faulted += OnFaulted;

				// 接続開始
				try
				{
					service.Open();
				}
                catch (CommunicationObjectFaultedException cofExc)
                {
                    // Faltedの状態のものを使用した場合は再生成する
                    // 本来はOnFaultedイベントで問題ないと思うのですが、
                    // 単体試験でOpen()エラーが連続で発生することがあったため、
                    // ここでも例外を補足し、下記のような再生成処理を行っています。
                    DisposeService();
                    this.CreateChannel(this._server_url);
                    throw cofExc;
                }
                catch (TimeoutException tex)
				{
					mostRecentEx = tex;
					// 接続タイムアウト
					throw tex;
				}
				finally
				{
				}
			}
		}

		/// <summary>
		/// クローズ
		/// </summary>
		public void Close()
		{
            if (_host == null) { return; }

            (_host as IChannel).Close();
		}

		/// <summary>
		/// クローズ完了イベント
		/// ※ Close()を呼出した後、呼ばれる。
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		protected virtual void OnClosed(object sender, EventArgs e)
		{
		}

		/// <summary>
		/// クローズ移行中イベント
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
        protected virtual void OnClosing(object sender, EventArgs e)
		{
		}

		/// <summary>
		/// 接続完了イベント
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
        protected virtual void OnOpened(object sender, EventArgs e)
		{
		}

		/// <summary>
		/// 異常イベント
		/// ※　ホストがいなくなるとイベントが来る。
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
        protected virtual void OnFaulted(object sender, EventArgs e)
		{
			DisposeService();
			this.CreateChannel(this._server_url);
		}

		/// <summary>
		/// Disposeサービス
		/// </summary>
		private void DisposeService()
		{
            var serviceChannel = _host as IClientChannel;
			if (serviceChannel == null)
			{
				return;
			}

			var success = false;
			try
			{
				serviceChannel.Closing -= this.OnClosing;
				serviceChannel.Closed -= this.OnClosed;
				serviceChannel.Opened -= this.OnOpened;
				serviceChannel.Faulted -= this.OnFaulted;
				if (serviceChannel.State != CommunicationState.Faulted)
				{
					serviceChannel.Close();
					success = true;
				}
                else
                {
                    serviceChannel.Abort();
                }
            }
            catch (CommunicationException)
            {
                serviceChannel.Abort();
            }
            catch (TimeoutException)
            {
                serviceChannel.Abort();
            }
            catch (Exception)
            {
                serviceChannel.Abort();
                throw;
			}
			finally
			{
				if (!success)
				{
					serviceChannel.Abort();
				}
				serviceChannel = null;
			}
		}
	}
}
